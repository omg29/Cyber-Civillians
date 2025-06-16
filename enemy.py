import pygame
import toolbox
import math
import random
from explosion import Explosion
from powerup import PowerUp
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("assets/Enemy_05.png")
        self.image1 = pygame.image.load("assets/Enemy_02.png")
        self.image2 = pygame.image.load("assets/Enemy_03.png")
        self.image3 = pygame.image.load("assets/Enemy_04.png")
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("assets/MediumExplosion1.png"))
        self.explosion_images.append(pygame.image.load("assets/MediumExplosion2.png"))
        self.explosion_images.append(pygame.image.load("assets/MediumExplosion3.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = 0
        self.speed = 0.5
        self.health = 20
        self.hurt_timer = 0
        self.damage = 1
        self.obstale_anger = 0
        self.obstale_anger_max = 100
        self.powerup_drop_chance = 50
        enemy_type = random.randint(0, 3)
        if enemy_type == 0:
            self.image = self.image
        elif enemy_type == 1:
            self.image = self.image1
        elif enemy_type == 2:
            self.image = self.image2
        elif enemy_type == 3:
            self.image = self.image3
        self.sfx_explode = pygame.mixer.Sound("assets/sfx/explosion-small.wav")
    def update(self, projectiles, crates, explosions):
        self.angle = toolbox.angleBetweenPoints(self.x, self.y, self.player.x, self.player.y)
        angle_rads = math.radians(self.angle)
        self.x_move = math.cos(angle_rads) * self.speed
        self.y_move = -math.sin(angle_rads) * self.speed
        test_rect = self.rect
        new_x = self.x + self.x_move
        new_y = self.y + self.y_move
        test_rect.center = (new_x, self.y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_x = self.x
                self.getAngry(crate)
        test_rect.center = (self.x, new_y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_y = self.y
                self.getAngry(crate)
        self.x = new_x
        self.y = new_y
        self.rect.center = (self.x, self.y)
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.getHit(projectile.damage)
                projectile.explode()
        for explosion in explosions:
            if explosion.damage:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)
        image_to_draw, image_rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.screen.blit(image_to_draw, image_rect)
    def getHit(self, damage):
        self.x -= self.x_move * 15
        self.y -= self.y_move * 15
        self.health -= damage
        if self.health <= 0:
            self.health = 99999
            self.sfx_explode.play()
            self.player.getScore(50)
            Explosion(self.screen, self.x, self.y, self.explosion_images, 20, 0, False)
            if random.randint(0, 100) < self.powerup_drop_chance:
                PowerUp(self.screen, self.x, self.y)    
            self.kill()
    def getAngry(self, crate):
        self.obstale_anger += 1
        if self.obstale_anger >= self.obstale_anger_max:
            crate.getHit(self.damage)
            self.obstale_angry = 0
