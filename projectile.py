import pygame
import toolbox
import math
from explosion import Explosion
class WaterBalloon(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, angle):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load("assets/Laser Sprites/02.png")
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("assets/SplashSmall1.png"))
        self.explosion_images.append(pygame.image.load("assets/SplashSmall2.png"))
        self.explosion_images.append(pygame.image.load("assets/SplashSmall3.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.speed = 10
        self.angle_rads = math.radians(self.angle)
        self.x_move = math.cos(self.angle_rads) * self.speed
        self.y_move = -math.sin(self.angle_rads) * self.speed
        self.damage = 6
        self.sfx_splash = pygame.mixer.Sound("assets/sfx/splash.wav")
    def update(self):
        self.x += self.x_move
        self.y += self.y_move
        self.rect.center = (self.x, self.y)
        if self.x < -self.image.get_width():
            self.kill()
        elif self.x > self.screen.get_width() + self.image.get_width():
            self.kill()
        elif self.y < -self.image.get_height():
            self.kill()
        elif self.y > self.screen.get_height() + self.image.get_height():
            self.kill()
        self.screen.blit(self.image, self.rect)
    def explode(self):
        Explosion(self.screen, self.x, self.y, self.explosion_images, 16, 0, False)
        self.sfx_splash.play()
        self.kill()
class SplitWaterBalloon(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load("assets/powerupSplit.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.damage = 3
class WaterDroplet(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load("assets/Laser Sprites/14.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.damage = 3
class ExplosiveWaterBalloon(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load("assets/Laser Sprites/42.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.explosion_images.append(pygame.image.load("assets/SplashLarge1.png"))
        self.explosion_images.append(pygame.image.load("assets/SplashLarge2.png"))
        self.explosion_images.append(pygame.image.load("assets/SplashLarge3.png"))
        self.sfx_splash_big = pygame.mixer.Sound("assets/sfx/splash-heavy.wav")
        self.damage = 20
        
    def explode(self):
        Explosion(self.screen, self.x, self.y, self.explosion_images, 16, 20, False)
        self.sfx_splash_big.play()
        self.kill()







        
