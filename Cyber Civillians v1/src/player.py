#player imports
import pygame
import random

#player sprite class
class Player(pygame.sprite.Sprite):
    #player initialize function
    def __init__ (self, screen, x, y):
        #player initialize
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.alive = True
        #player images
        self.playerImage1 = pygame.image.load("../assets/")
        self.playerImage2 = pygame.image.load("../assets/")
        self.playerImage3 = pygame.image.load("../assets/")
        #player rect
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 50
        self.animation_speed = 30
    #update function
    def update(self):
        self.rect.center = (self.x, self.y)

    #player movement function
    def move(self, x_movement, y_movement):
        if self.alive:
            test_rect = self.rect
            test_rect.x += self.speed * x_movement
            test_rect.y += self.speed * y_movement
            collision = False
            if not collision:
                self.x = self.speed * x_movement
                self.y = self.speed * y_movement