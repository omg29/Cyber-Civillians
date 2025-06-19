#import all libraries
import pygame                        # Main game library for graphics and sound
import random                        # For randomness (e.g., random crate spawns, etc.)
import toolbox                       # Custom helper functions (like rotation or angle calculations)
import projectile                    # Contains classes for projectiles (WaterBalloon, etc.)

#import all files
from crate import Crate             # Import basic crate class
from crate import ExplosiveCrate    # Import explosive crate class

#player class
class Player(pygame.sprite.Sprite):    # Player is a sprite (movable object in the game)
    
    #initialize function
    def __init__(self, screen, x, y):     # Called when you create a Player
        pygame.sprite.Sprite.__init__(self, self.containers)  # Add to sprite group
        self.screen = screen              # Save the game screen to draw on it later
        self.x = x                        # X position
        self.y = y                        # Y position
        
        #load and choose self.image
        self.image = pygame.image.load("assets/Player.png")            # Load player image
        self.image_defeated = pygame.image.load("assets/Enemy_01.png") # Image if player dies

        #player rect
        self.rect = self.image.get_rect()        # Get rectangle around player image
        self.rect.center = (self.x, self.y)      # Set starting position

        #player properties
        self.speed = 8                 # Movement speed
        self.angle = 0                 # Angle the player is aiming
        self.shoot_cooldown = 0       # Time between shots
        self.shoot_cooldown_max = 10  # Max cooldown before shooting again

        #player health
        self.health_max = 75                  # Max health
        self.health = self.health_max         # Start at full health
        self.health_bar_width = self.image.get_width()  # Health bar is as wide as the image
        self.health_bar_height = 8                     # Fixed height for health bar
        self.health_bar_green = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)  # Green part
        self.health_bar_red = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)    # Red background

        #ammo type and crate amounts
        self.alive = True                    # Is player alive
        self.crate_ammo = 10                 # Number of normal crates
        self.explosive_crate_ammo = 10       # Number of explosive crates
        self.crate_cooldown = 0              # Time before another crate can be placed
        self.crate_cooldown_max = 10         # Max cooldown for crates
        self.shot_type = 'normal'            # Type of ammo
        self.special_ammo = 0                # Amount of special ammo (used for special shots)
        self.score = 0                       # Player score

        #import all sound effects
        self.sfx_shot = pygame.mixer.Sound("assets/sfx/shot.wav")               # Sound when shooting
        self.sfx_place = pygame.mixer.Sound("assets/sfx/bump.wav")              # Sound when placing crate
        self.sfx_defeat = pygame.mixer.Sound("assets/sfx/electrocute.wav")      # Sound on death
        self.sfx_damage = pygame.mixer.Sound("assets/sfx/damage.wav")           # Sound when hit
        self.sfx_cratea = pygame.mixer.Sound("assets/sfx/cratesa.wav")          # Crate power-up sound
        self.sfx_ecratesa = pygame.mixer.Sound("assets/sfx/ecratesa.wav")       # Explosive crate power-up
        self.sfx_streama = pygame.mixer.Sound("assets/sfx/streama.wav")         # Stream shot power-up
        self.sfx_bursta = pygame.mixer.Sound("assets/sfx/bursta.wav")           # Burst shot power-up
        self.sfx_nocratesa = pygame.mixer.Sound("assets/sfx/nocratesa.wav")     # Out of normal crates
        self.sfx_noecratesa = pygame.mixer.Sound("assets/sfx/noecratesa.wav")   # Out of explosive crates

        #player energy
        self.energy = 1000                              # Energy for movement
        self.hud_font = pygame.font.SysFont('adobedevanagaribolditaliconpentype', 30)  # Font for energy display
        self.energy_text = self.hud_font.render("Beep boop", True, (255, 255, 255))    # Starting HUD text
    
    #update function
    def update(self, enemies, explosions):     # Runs every frame to update the player
        self.rect.center = (self.x, self.y)    # Update position

        #check if player hit by an explosion
        for explosion in explosions:
            if explosion.damage and explosion.damage_player:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)   # Take damage

        #check if plater hit by an enemy  
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.getHit(0)               # Damage enemy slightly
                self.getHit(enemy.damage)     # Take enemy damage

        #player cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.crate_cooldown > 0:
            self.crate_cooldown -= 1 

        #keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()

        #positioning and getting the angle between the player and mouse    
        self.x = self.rect.centerx
        self.y = self.rect.centery
        if self.alive:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.angle = toolbox.angleBetweenPoints(self.x, self.y, mouse_x, mouse_y)
        if self.alive:
            pass
        else:
            #defeated image
            self.image = self.image_defeated 

        #rotate and show the image from the angle    
        image_to_draw, image_rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.screen.blit(image_to_draw, image_rect)

        #draw health bar
        self.health_bar_red.x = self.rect.x
        self.health_bar_red.bottom = self.rect.y - 5
        pygame.draw.rect(self.screen, (255, 0, 0 ), self.health_bar_red)
        self.health_bar_green.topleft = self.health_bar_red.topleft
        health_percentage = self.health / self.health_max
        self.health_bar_green.width = self.health_bar_width * health_percentage
        if self.alive:
            pygame.draw.rect(self.screen, (0, 255,0), self.health_bar_green)

        #make sure energy is never negative
        if self.energy < 0:
            self.energy = 0

        #show player energy on screen
        self.energy_text = self.hud_font.render("Energy: " + str(self.energy), True, (255, 255, 255))
        self.screen.blit(self.energy_text, (10, 50))
        
    #player movement function        
    def move(self, x_movement, y_movement, crates):
        if self.alive:
            #check using test rect for collisions with crates
            test_rect = self.rect
            test_rect.x += self.speed * x_movement
            test_rect.y += self.speed * y_movement
            collision = False
            for crate in crates:
                if not crate.just_placed:
                    if test_rect.colliderect(crate.rect):
                        collision = True
            
            #move the player if self.energy > 0 and no collision
            if not collision:
                if self.energy > 0:
                    self.x += self.speed * x_movement
                    self.y += self.speed * y_movement
                    self.energy -= 1

    #player shooting function
    def shoot(self):
        if self.shoot_cooldown <= 0 and self.alive:
            self.sfx_shot.play()  # play shooting sound
            if self.shot_type == 'normal':
                projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
            elif self.shot_type == 'split' and self.special_ammo <= 0:
                projectile.SplitWaterBalloon(self.screen, self.x, self.y, self.angle - 15)
                projectile.SplitWaterBalloon(self.screen, self.x, self.y, self.angle)
                projectile.SplitWaterBalloon(self.screen, self.x, self.y, self.angle + 15)
                self.special_ammo -= 1
            elif self.shot_type == 'stream':
                projectile.WaterDroplet(self.screen, self.x, self.y, self.angle)
                self.special_ammo -= 1
            elif self.shot_type == 'burst':
                projectile.ExplosiveWaterBalloon(self.screen, self.x, self.y, self.angle)
                self.special_ammo -= 1
            self.shoot_cooldown = self.shoot_cooldown_max
            if self.special_ammo <= 0:
                self.shot_type = 'normal'
                self.shoot_cooldown_max = 10
                self.shoot_cooldown = self.shoot_cooldown_max

    #player gets hit
    def getHit(self, damage):
        if self.alive:
            self.sfx_damage.play()
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self.sfx_defeat.play()

    #place normal crate
    def placeCrate(self):
        if self.alive and self.crate_ammo > 0 and self.crate_cooldown <= 0:
            Crate(self.screen, self.x, self.y, self)
            self.crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max
            self.sfx_place.play()
        if self.crate_ammo == 0:
            self.sfx_nocratesa.play()

    #place explosive crate
    def placeExplosiveCrate(self):
        if self.alive and self.explosive_crate_ammo > 0 and self.crate_cooldown <= 0:
            ExplosiveCrate(self.screen, self.x, self.y, self)
            self.explosive_crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max
            self.sfx_place.play()
        if self.explosive_crate_ammo == 0:
            self.sfx_noecratesa.play()

    #activate power up
    def powerUp(self, power_type):
        if power_type == 'crateammo':
            self.sfx_cratea.play()
            self.crate_ammo += 10
            self.getScore(10)
        elif power_type == 'explosiveammo':
            self.explosive_crate_ammo += 10
            self.getScore(10)
            self.sfx_ecratesa.play()
        elif power_type == 'split':
            self.shot_type = 'split'
            special_ammo = 40
            self.getScore(20)
            self.shoot_cooldown_max = 20
        elif power_type == 'normal':
            self.shot_type = 'normal'
            self.shoot_cooldown_max = 10
        elif power_type == 'stream':
            self.shot_type = 'stream'
            self.special_ammo = 300
            self.shoot_cooldown_max = 3
            self.getScore(20)
            self.sfx_streama.play()
        elif power_type == 'burst':
            self.shot_type = 'burst'
            self.special_ammo = 35
            self.shoot_cooldown_max = 50
            self.getScore(20)
            self.sfx_bursta.play()

    #increase score
    def getScore(self, score):
        if self.alive:
            self.score += score
