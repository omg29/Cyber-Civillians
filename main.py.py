#import all libraries
import pygame
import random
from pygame import mixer
from player import Player

#import all files
from projectile import WaterBalloon
from enemy import Enemy
from crate import Crate
from crate import ExplosiveCrate
from explosion import Explosion
from powerup import PowerUp
from hud import HUD
#make the game
pygame.init()
pygame.mixer.pre_init(buffer=1024)
game_width = 1000
game_height = 600
screen = pygame.display.set_mode((game_width, game_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
game_started = False

#all sprite groups
playerGroup = pygame.sprite.Group()
projectilesGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
cratesGroup = pygame.sprite.Group()
explosionsGroup = pygame.sprite.Group()
powerupsGroup = pygame.sprite.Group()
Player.containers = playerGroup
WaterBalloon.containers = projectilesGroup
Enemy.containers = enemiesGroup
Crate.containers = cratesGroup
Explosion.containers = explosionsGroup
PowerUp.containers = powerupsGroup

#spawn enemies
enemy_spawn_timer_max = 100
enemy_spawn_timer = 0
enemy_spawn_speedup_timer_max = 400
enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

#make player
mr_player = Player(screen, game_width/2, game_height/2)
hud = HUD(screen, mr_player)

#start the game
def StartGame():
    global game_started
    game_started = True
    global hud
    hud.state = 'ingame'
    global mr_player
    mr_player.__init__(screen, game_width/2, game_height/2)
    global enemy_spawn_timer_max
    global enemy_spawn_timer
    global enemy_spawn_speedup_timer
    enemy_spawn_timer_max = 100
    enemy_spawn_timer = 0
    enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max
    for i in range(0, 10):
        ExplosiveCrate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)
        Crate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)

#load and choose background
background_image = pygame.image.load("assets/jordon-lee-3.jpg")
background_image = background_image

#background
#mixer.music.load('assets/sfx/backgroundmusic.mp3')
#mixer.music.play(-1)

#==================================================================================================================================#
#-------------------------------------------------------------Loop Land------------------------------------------------------------#
#==================================================================================================================================#
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    screen.blit(background_image, (0, 0))
    if not game_started:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                StartGame()
                break

    #in game function
    if game_started:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            mr_player.move(1, 0, cratesGroup)
        if keys[pygame.K_a]:
            mr_player.move(-1, 0, cratesGroup)
        if keys[pygame.K_w]:
            mr_player.move(0, -1, cratesGroup)
        if keys[pygame.K_s]:
            mr_player.move(0, 1, cratesGroup)
        if pygame.mouse.get_pressed()[0]:
            mr_player.shoot()
        if keys[pygame.K_SPACE]:
            mr_player.placeCrate()
        if pygame.mouse.get_pressed()[2]:
            mr_player.placeExplosiveCrate()



        if enemy_spawn_speedup_timer <= 0:
            if enemy_spawn_timer_max > 20:
                enemy_spawn_timer_max -= 10
            enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max
        enemy_spawn_timer -= 1

        #decide which side to spawn enemy
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy(screen, 0, 0, mr_player)
            side_to_spawn = random.randint(0,3)
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

        #update all groups
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

        #reset funcion
        if not mr_player.alive:
            if hud.state == 'ingame':
                hud.state = 'gameover'
            elif hud.state == 'mainmenu':
                game_started = False
                playerGroup.empty()
                enemiesGroup.empty()
                projectilesGroup.empty()
                powerupsGroup.empty()
                explosionsGroup.empty()
                cratesGroup.empty()

    #game funcitons
    hud.update()
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("Cyber Civillians fps: " + str(clock.get_fps()))

