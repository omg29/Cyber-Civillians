import pygame
import random
from explosion import Explosion 
class Crate(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("assets/Crate.png")
        self.image1 = pygame.image.load("assets/Barrel.png")
        crate_type = random.randint(0, 1)
        if crate_type == 0:
            self.image = self.image
        elif crate_type ==1:
            self.image = self.image1
        self.explosion_images = []
        if crate_type ==0:
            self.explosion_images.append(pygame.image.load('assets/CrateRubble.png'))
        if crate_type ==1:
            self.explosion_images.append(pygame.image.load('assets/BarrelRubble.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.health = 50
        self.hurt_timer = 0
        self.just_placed = True
        self.sfx_break = pygame.mixer.Sound("assets/sfx/break.wav")
    def update(self, projectiles, explosions):
        if not self.rect.colliderect(self.player.rect):
            self.just_placed = False
        for explosion in explosions:
            if explosion.damage:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.getHit(projectile.damage)
        self.screen.blit(self.image, self.rect)
    def getHit(self, damage):
        self.health -= damage
        self.hurt_timer = 5
        if self.health <= 0:
            self.sfx_break.play()
            Explosion(self.screen, self.x, self.y, self.explosion_images, 80, 0, False)
            self.health = 99999
            self.kill()
class ExplosiveCrate(Crate):
    def __init__(self, screen, x, y, player):
        Crate.__init__(self, screen, x, y, player)
        self.image = pygame.image.load("assets/ExplosiveBarrel.png")
        self.image1 = pygame.image.load("assets/ExplosiveCrate.png")
        crate_type = random.randint(0, 1)
        if crate_type == 0:
            self.image = self.image
        elif crate_type == 1:
            self.image = self.image1
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("assets/LargeExplosion1.png"))
        self.explosion_images.append(pygame.image.load("assets/LargeExplosion2.png"))
        self.explosion_images.append(pygame.image.load("assets/LargeExplosion3.png"))
        self.health = 20
        self.sfx_explode = pygame.mixer.Sound("assets/sfx/explosion-big.wav")
    def getHit(self, damage):
        self.health -= damage
        self.hurt_timer = 5
        if self.health <= 0:
            self.sfx_explode.play()
            Explosion(self.screen, self.x, self.y, self.explosion_images, 20, 4, True)
            self.health = 99999
            self.kill()
