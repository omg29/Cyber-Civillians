import pygame
import random
import toolbox
import projectile
from crate import Crate
from crate import ExplosiveCrate
class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.image1 = pygame.image.load("assets/Player_01.png")
        self.image2 = pygame.image.load("assets/Player_02.png")
        self.image3 = pygame.image.load("assets/Player_03.png")
        self.image4 = pygame.image.load("assets/Player_04.png")
        self.image5 = pygame.image.load("assets/Player_05.png")
        player_image = random.randint(0, 4)
        if player_image == 0:
            self.image = self.image1
        if player_image == 1:
            self.image = self.image2
        if player_image == 2:
            self.image = self.image3
        if player_image == 3:
            self.image = self.image4
        if player_image == 4:
            self.image = self.image5
        self.image_defeated = pygame.image.load("assets/Enemy_01.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 8
        self.angle = 0
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 10
        self.health_max = 75
        self.health = self.health_max
        self.health_bar_width = self.image.get_width()
        self.health_bar_height = 8
        self.health_bar_green = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        self.health_bar_red = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        self.alive = True
        self.crate_ammo = 10
        self.explosive_crate_ammo = 10
        self.crate_cooldown = 0
        self.crate_cooldown_max = 10
        self.shot_type = 'normal'
        self.special_ammo = 0
        self.score = 0
        self.sfx_shot = pygame.mixer.Sound("assets/sfx/shot.wav")
        self.sfx_place = pygame.mixer.Sound("assets/sfx/bump.wav")
        self.sfx_defeat = pygame.mixer.Sound("assets/sfx/electrocute.wav")
        self.sfx_damage = pygame.mixer.Sound("assets/sfx/damage.wav")
        self.sfx_cratea = pygame.mixer.Sound("assets/sfx/cratesa.wav")
        self.sfx_ecratesa = pygame.mixer.Sound("assets/sfx/ecratesa.wav")
        self.sfx_streama = pygame.mixer.Sound("assets/sfx/streama.wav")
        self.sfx_bursta = pygame.mixer.Sound("assets/sfx/bursta.wav")
        self.sfx_nocratesa = pygame.mixer.Sound("assets/sfx/nocratesa.wav")
        self.sfx_noecratesa = pygame.mixer.Sound("assets/sfx/noecratesa.wav")
        self.energy = 2000
        self.hud_font = pygame.font.SysFont('adobedevanagaribolditaliconpentype', 30)
        self.energy_text = self.hud_font.render("Beep boop", True, (255, 255, 255))
    
    def update(self, enemies, explosions):
        self.rect.center = (self.x, self.y)
        for explosion in explosions:
            if explosion.damage and explosion.damage_player:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)   
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.getHit(0)
                self.getHit(enemy.damage)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.crate_cooldown > 0:
            self.crate_cooldown -= 1 
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
        self.x = self.rect.centerx
        self.y = self.rect.centery
        if self.alive:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.angle = toolbox.angleBetweenPoints(self.x, self.y, mouse_x, mouse_y)
        if self.alive:
            pass
        else:
            self.image = self.image_defeated 
        image_to_draw, image_rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.screen.blit(image_to_draw, image_rect)
        self.health_bar_red.x = self.rect.x
        self.health_bar_red.bottom = self.rect.y - 5
        pygame.draw.rect(self.screen, (255, 0, 0 ), self.health_bar_red)
        self.health_bar_green.topleft = self.health_bar_red.topleft
        health_percentage = self.health / self.health_max
        self.health_bar_green.width = self.health_bar_width * health_percentage
        if self.alive:
            pygame.draw.rect(self.screen, (0, 255,0), self.health_bar_green)
        if self.energy < 0:
            self.energy = 0
        self.energy_text = self.hud_font.render("Energy: " + str(self.energy), True, (255, 255, 255))
        self.screen.blit(self.energy_text, (10, 50))
        
            
    def move(self, x_movement, y_movement, crates):
        if self.alive:
            test_rect = self.rect
            test_rect.x += self.speed * x_movement
            test_rect.y += self.speed * y_movement
            collision = False
            for crate in crates:
                if not crate.just_placed:
                    if test_rect.colliderect(crate.rect):
                        collision = True
            if not collision:
                if self.energy > 0:
                    self.x += self.speed * x_movement
                    self.y += self.speed * y_movement
                    self.energy -= 1

    def shoot(self):
        if self.shoot_cooldown <= 0 and self.alive:
            self.sfx_shot.play()
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
    def getHit(self, damage):
        if self.alive:
            self.sfx_damage.play()
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self.sfx_defeat.play()
    def placeCrate(self):
        if self.alive and self.crate_ammo > 0 and self.crate_cooldown <= 0:
            Crate(self.screen, self.x, self.y, self)
            self.crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max
            self.sfx_place.play()
        if self.crate_ammo == 0:
            self.sfx_nocratesa.play()

    def placeExplosiveCrate(self):
        if self.alive and self.explosive_crate_ammo > 0 and self.crate_cooldown <= 0:
            ExplosiveCrate(self.screen, self.x, self.y, self)
            self.explosive_crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max
            self.sfx_place.play()
        if self.explosive_crate_ammo == 0:
            self.sfx_noecratesa.play()
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
    def getScore(self, score):
        if self.alive:
            self.score += score

