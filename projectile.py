import pygame
import toolbox
import math
from explosion import Explosion

class WaterBalloon(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, angle):
        pygame.sprite.Sprite.__init__(self, self.containers)  # Initialize sprite
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = angle
        
        # Load the balloon image
        self.image = pygame.image.load("assets/Laser Sprites/02.png")
        
        # Load images for small splash explosion animation
        self.explosion_images = [
            pygame.image.load("assets/SplashSmall1.png"),
            pygame.image.load("assets/SplashSmall2.png"),
            pygame.image.load("assets/SplashSmall3.png")
        ]
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        # Rotate the balloon image based on the angle it's fired at
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        
        self.speed = 10  # Speed of balloon movement
        
        # Convert angle to radians for movement calculations
        self.angle_rads = math.radians(self.angle)
        
        # Calculate how much to move each frame in x and y directions
        self.x_move = math.cos(self.angle_rads) * self.speed
        self.y_move = -math.sin(self.angle_rads) * self.speed
        
        self.damage = 6  # Damage the balloon deals
        
        # Sound effect for splash
        self.sfx_splash = pygame.mixer.Sound("assets/sfx/splash.wav")
    
    def update(self):
        # Move the balloon
        self.x += self.x_move
        self.y += self.y_move
        self.rect.center = (self.x, self.y)
        
        # Remove the balloon if it goes off-screen (with some padding)
        if self.x < -self.image.get_width():
            self.kill()
        elif self.x > self.screen.get_width() + self.image.get_width():
            self.kill()
        elif self.y < -self.image.get_height():
            self.kill()
        elif self.y > self.screen.get_height() + self.image.get_height():
            self.kill()
        
        # Draw the balloon on screen
        self.screen.blit(self.image, self.rect)
    
    def explode(self):
        # Create explosion effect and play splash sound, then remove balloon
        Explosion(self.screen, self.x, self.y, self.explosion_images, 16, 0, False)
        self.sfx_splash.play()
        self.kill()

class SplitWaterBalloon(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)  # Call parent constructor
        
        # Use different image for split balloon
        self.image = pygame.image.load("assets/powerupSplit.png")
        self.rect = self.image.get_rect()
        
        # Rotate the image to match the angle
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        
        self.damage = 3  # Deals less damage than normal balloon

class WaterDroplet(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        
        # Use droplet image
        self.image = pygame.image.load("assets/Laser Sprites/14.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        
        self.damage = 3  # Lower damage

class ExplosiveWaterBalloon(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        
        # Use explosive balloon image
        self.image = pygame.image.load("assets/Laser Sprites/42.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        
        # Add bigger splash images for explosion animation
        self.explosion_images.append(pygame.image.load("assets/SplashLarge1.png"))
        self.explosion_images.append(pygame.image.load("assets/SplashLarge2.png"))
        self.explosion_images.append(pygame.image.load("assets/SplashLarge3.png"))
        
        # Load big splash sound effect
        self.sfx_splash_big = pygame.mixer.Sound("assets/sfx/splash-heavy.wav")
        
        self.damage = 20  # Much higher damage
    
    def explode(self):
        # Create big explosion, play big splash sound, and remove balloon
        Explosion(self.screen, self.x, self.y, self.explosion_images, 16, 20, False)
        self.sfx_splash_big.play()
        self.kill()







        
