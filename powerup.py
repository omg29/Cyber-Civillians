import pygame
import random
import toolbox
from player import Player

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)  # Initialize sprite
        self.screen = screen
        self.x = x
        self.y = y
        
        # Pick a random power-up type (0 to 3)
        self.pick_power = random.randint(0, 3)
        
        # Set images and power type based on random pick
        if self.pick_power == 0:
            self.image = pygame.image.load("assets/powerupCrate.png")
            self.background_image = pygame.image.load("assets/powerupBackgroundBlue.png")
            self.power_type = 'crateammo'
        elif self.pick_power == 1:
            self.image = pygame.image.load("assets/powerupExplosiveBarrel.png")
            self.background_image = pygame.image.load("assets/powerupBackgroundBlue.png")
            self.power_type = 'explosiveammo'
        elif self.pick_power == 2:
            self.image = pygame.image.load("assets/Laser Sprites/14.png")
            self.background_image = pygame.image.load("assets/powerupBackgroundRed.png")
            self.power_type = 'stream'
        elif self.pick_power == 3:
            self.image = pygame.image.load("assets/Laser Sprites/42.png")
            self.background_image = pygame.image.load("assets/powerupBackgroundRed.png")
            self.power_type = 'burst'
        
        self.rect = self.image.get_rect()       # Get image size and shape
        self.rect.center = (self.x, self.y)     # Place power-up at (x, y)
        
        self.background_angle = 0                # Angle for spinning background
        self.spinny_speed = 2                    # Speed of spinning
        
        self.despawn_timer = 400                 # How long power-up stays before disappearing
        
        # Load sounds
        self.sfx_pickup = pygame.mixer.Sound("assets/sfx/powerup.wav")
        self.sfx_right = pygame.mixer.Sound("assets/sfx/puright.wav")
    
    def update(self, player):
        # If player touches power-up, apply it and remove power-up
        if self.rect.colliderect(player.rect):
            self.sfx_pickup.play()
            player.powerUp(self.power_type)
            self.kill()
        
        # Countdown until power-up disappears
        self.despawn_timer -= 1
        if self.despawn_timer <= 0:
            self.kill()
        
        # Spin the background image
        self.background_angle += self.spinny_speed
        
        # Get rotated background image
        bg_image_to_draw, bg_rect = toolbox.getRotatedImage(self.background_image, self.rect, self.background_angle)
        
        # Draw background and power-up; blink near despawn time
        if self.despawn_timer > 120 or self.despawn_timer % 10 > 5:
            self.screen.blit(bg_image_to_draw, bg_rect)
            self.screen.blit(self.image, self.rect)


