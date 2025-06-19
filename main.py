#import all libraries
import pygame                         # Main game library
import random                         # For random positioning
from pygame import mixer              # For music and sound effects
from player import Player             # Import Player class

#import all files
from projectile import WaterBalloon   # WaterBalloon projectile
from enemy import Enemy               # Enemy class
from enemy import Boss                # Boss class
from crate import Crate               # Basic crate
from crate import ExplosiveCrate      # Explosive crate
from explosion import Explosion       # Explosion effects
from powerup import PowerUp           # Power-up items
from hud import HUD                   # Heads-up display

#make the game
pygame.init()                         # Initialize pygame
pygame.mixer.pre_init(buffer=1024)   # Pre-initialize sound system

# Game screen size
game_width = 1000
game_height = 600
screen = pygame.display.set_mode((game_width, game_height), pygame.RESIZABLE)  # Create resizable screen window
clock = pygame.time.Clock()          # Game clock to control FPS
running = True                       # Flag to keep the game running
game_started = False                 # Flag to track if the game has started

#all sprite groups
playerGroup = pygame.sprite.Group()        # Group for player sprites
projectilesGroup = pygame.sprite.Group()   # Group for projectile sprites
enemiesGroup = pygame.sprite.Group()       # Group for enemy sprites
cratesGroup = pygame.sprite.Group()        # Group for crate sprites
explosionsGroup = pygame.sprite.Group()    # Group for explosion sprites
powerupsGroup = pygame.sprite.Group()      # Group for power-up sprites

#all container groups (so each class knows where to add new sprites)
Player.containers = playerGroup
WaterBalloon.containers = projectilesGroup
Enemy.containers = enemiesGroup
Crate.containers = cratesGroup
Explosion.containers = explosionsGroup
PowerUp.containers = powerupsGroup

#spawn enemies timers and speedup mechanics
enemy_spawn_timer_max = 100              # Time between enemy spawns (decreases over time to spawn faster)
enemy_spawn_timer = 0
enemy_spawn_speedup_timer_max = 400     # Timer for how often spawn rate speeds up
enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

# Boss spawn variables added
bossSpawnTimer = 0
bossSpawnTimerMax = 2400

#make player
mr_player = Player(screen, game_width/2, game_height/2)   # Create player in the center of the screen
hud = HUD(screen, mr_player)                             # Initialize HUD to show health, score, etc.

#start the game function (called to reset and start gameplay)
def StartGame():
    global game_started
    game_started = True            # Set game as started
    global hud
    hud.state = 'ingame'           # Change HUD state to in-game
    global mr_player
    mr_player.__init__(screen, game_width/2, game_height/2)   # Reset player position and state
    global enemy_spawn_timer_max
    global enemy_spawn_timer
    global enemy_spawn_speedup_timer
    enemy_spawn_timer_max = 100    # Reset enemy spawn timer max
    enemy_spawn_timer = 0          # Reset enemy spawn timer
    enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max   # Reset speedup timer

    #spawn crates and explosive crates randomly on map
    for i in range(0, 10):
        ExplosiveCrate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)
        Crate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)

#load and choose background image
background_image = pygame.image.load("assets/cyberpunk2.jpg")

#question cooldown timer to control how often question screen toggles
questionScreenCoolDown = 0
questionScreenCoolDownMax = 20

#quetions anwering timer to control how oftern you can answer the question
questionAnswerCoolDown = 0
QuetionAnswerCoolDownMax = 20

#background music (commented out, but ready to use)
#mixer.music.load('assets/sfx/backgroundmusic.mp3')
#mixer.music.play(-1)

#==================================================================================================================================#
#-------------------------------------------------------------Loop Land------------------------------------------------------------#
#==================================================================================================================================#

while running:
    # Event handling: quit or ESC key to close game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(background_image, (0, 0))   # Draw background each frame

    if not game_started:
        events = pygame.event.get()
        StartGame()                         # Start the game if not started
        for event in events:
            if event.type == pygame.KEYDOWN:
                StartGame()                 # Restart game on any key press
                break

    #in game controls and updates
    if game_started:
        #move player with WASD keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            mr_player.move(1, 0, cratesGroup)
        if keys[pygame.K_a]:
            mr_player.move(-1, 0, cratesGroup)
        if keys[pygame.K_w]:
            mr_player.move(0, -1, cratesGroup)
        if keys[pygame.K_s]:
            mr_player.move(0, 1, cratesGroup)
        
        #other player controls
        if pygame.mouse.get_pressed()[0]:   # Left click to shoot
            mr_player.shoot()
        if keys[pygame.K_SPACE]:            # Space to place crate
            mr_player.placeCrate()
        if pygame.mouse.get_pressed()[2]:   # Right click to place explosive crate
            mr_player.placeExplosiveCrate()
        if keys[pygame.K_LSHIFT] and questionScreenCoolDown < 0:  # Left Shift toggles question screen
            if hud.showQuestions == False:
                hud.showQuestions = True
                questionScreenCoolDown = questionScreenCoolDownMax
            else:
                hud.showQuestions = False
                questionScreenCoolDown = questionScreenCoolDownMax
        if questionAnswerCoolDown < 0:
            if keys[pygame.K_1]:
                hud.answerQuestion(1)
                questionAnswerCoolDown = questionScreenCoolDownMax
            elif keys[pygame.K_2]:
                hud.answerQuestion(2)
                questionAnswerCoolDown = questionScreenCoolDownMax
            elif keys[pygame.K_3]:
                hud.answerQuestion(3)
                questionAnswerCoolDown = questionScreenCoolDownMax
            elif keys[pygame.K_4]:
                hud.answerQuestion(4)
                questionAnswerCoolDown = questionScreenCoolDownMax

        #speed up enemy spawn timer over time
        if enemy_spawn_speedup_timer <= 0:
            if enemy_spawn_timer_max > 20:   # Minimum spawn delay is 20 frames
                enemy_spawn_timer_max -= 10
            enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max
        enemy_spawn_timer -= 1

        #spawn enemies on random sides when timer runs out
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy(screen, 0, 0, mr_player)
            side_to_spawn = random.randint(0,3)  # Choose side to spawn (0=top,1=bottom,2=left,3=right)
            if side_to_spawn == 0:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = -new_enemy.image.get_height()
            elif side_to_spawn == 1:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = game_height + new_enemy.image.get_height()
            elif side_to_spawn == 2:
                new_enemy.x = -new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
            elif side_to_spawn == 3:
                new_enemy.x = game_width + new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
            enemy_spawn_timer = enemy_spawn_timer_max
        #Boss Spawn logic
        bossSpawnTimer += 1
        if bossSpawnTimer >= bossSpawnTimerMax:
            boss = Boss(screen, 500, 300, mr_player)
            bossSpawnTimer = 0

        #cool down for question screen toggle
        questionScreenCoolDown -= 1    
        questionAnswerCoolDown -= 1

        #update all game objects
        for powerup in powerupsGroup:
            powerup.update(mr_player)
        for explosion in explosionsGroup:
            explosion.update()
        for projectile in projectilesGroup:   
            projectile.update()
        for enemy in enemiesGroup:
            enemy.update(projectilesGroup, cratesGroup, explosionsGroup)
        for crate in cratesGroup:
            crate.update(projectilesGroup, explosionsGroup)
            for explosion in explosionsGroup:
                explosion.update()    
        mr_player.update(enemiesGroup, explosionsGroup)

        #handle player death and reset game states
        if not mr_player.alive:
            if hud.state == 'ingame':
                hud.state = 'gameover'
            elif hud.state == 'mainmenu':
                game_started = False
                # Clear all sprite groups for next game
                playerGroup.empty()
                enemiesGroup.empty()
                projectilesGroup.empty()
                powerupsGroup.empty()
                explosionsGroup.empty()
                cratesGroup.empty()

    #update HUD and flip display buffer
    hud.update()
    pygame.display.flip()
    clock.tick(40)   # Limit to 40 frames per second
    pygame.display.set_caption("Cyber Civillians fps: " + str(clock.get_fps()))
