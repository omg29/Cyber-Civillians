import pygame
import random
from explosion import Explosion 

class Crate(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        # Initialize the sprite and add it to all relevant sprite groups
        pygame.sprite.Sprite.__init__(self, self.containers)  
        
        self.screen = screen          # The game screen where the crate will be drawn
        self.x = x                    # X coordinate of the crate
        self.y = y                    # Y coordinate of the crate
        self.player = player          # Reference to the player (to check collisions)
        
        # Load two types of crate images to randomly choose from
        self.image = pygame.image.load("assets/Crate.png")  
        self.image1 = pygame.image.load("assets/Barrel.png") 
        
        crate_type = random.randint(0, 1)  # Randomly choose crate appearance
        
        # Set the crate image based on the random type chosen
        if crate_type == 0:
            self.image = self.image
        elif crate_type == 1:
            self.image = self.image1
        
        # Prepare the rubble images for the crate’s destruction animation
        self.explosion_images = []
        if crate_type == 0:
            self.explosion_images.append(pygame.image.load('assets/CrateRubble.png'))
        if crate_type == 1:
            self.explosion_images.append(pygame.image.load('assets/BarrelRubble.png'))
        
        # Get the rectangle for positioning and collision detection
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.health = 50              # How much damage the crate can take before breaking
        self.hurt_timer = 0           # Timer to handle hit effects (not shown here)
        self.just_placed = True       # Track if crate was just placed to avoid immediate collision
        self.sfx_break = pygame.mixer.Sound("assets/sfx/break.wav")  # Sound when crate breaks

    def update(self, projectiles, explosions):
        # If player moves away from crate, it’s no longer "just placed"
        if not self.rect.colliderect(self.player.rect):
            self.just_placed = False
        
        # Check if crate is hit by explosions, reduce health accordingly
        for explosion in explosions:
            if explosion.damage:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)

        # Check if crate is hit by projectiles, reduce health accordingly
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.getHit(projectile.damage)

        # Draw the crate image on the screen at its current position
        self.screen.blit(self.image, self.rect)

    def getHit(self, damage):
        self.health -= damage        # Reduce crate health by the damage amount
        self.hurt_timer = 5          # Set timer for hurt effect (not visualized here)
        
        # If crate health reaches zero or below, play break sound and explode
        if self.health <= 0:
            self.sfx_break.play()    # Play breaking sound effect
            
            # Create a rubble explosion effect at the crate’s position
            Explosion(self.screen, self.x, self.y, self.explosion_images, 80, 0, False)
            
            self.health = 99999      # Prevent further damage after it’s destroyed
            self.kill()              # Remove crate from all sprite groups (disappear)

class ExplosiveCrate(Crate):
    def __init__(self, screen, x, y, player):
        # Initialize as a normal crate first
        Crate.__init__(self, screen, x, y, player)
        
        # Load images for explosive crate variants
        self.image = pygame.image.load("assets/ExplosiveBarrel.png")
        self.image1 = pygame.image.load("assets/ExplosiveCrate.png")
        
        crate_type = random.randint(0, 1)  # Randomly choose explosive crate appearance
        
        # Assign image based on crate type
        if crate_type == 0:
            self.image = self.image
        elif crate_type == 1:
            self.image = self.image1
        
        # Load larger explosion images for the explosive crate’s destruction
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("assets/LargeExplosion1.png"))
        self.explosion_images.append(pygame.image.load("assets/LargeExplosion2.png"))
        self.explosion_images.append(pygame.image.load("assets/LargeExplosion3.png"))
        
        self.health = 20                         # Explosive crates have less health (break faster)
        self.sfx_explode = pygame.mixer.Sound("assets/sfx/explosion-big.wav")  # Big explosion sound

    def getHit(self, damage):
        self.health -= damage            # Decrease health by damage amount
        self.hurt_timer = 5              # Set hurt timer for hit effects
        
        # If health is zero or less, play explosion sound and trigger explosion
        if self.health <= 0:
            self.sfx_explode.play()      # Play big explosion sound
            
            # Create a big explosion that deals damage and can hurt the player too
            Explosion(self.screen, self.x, self.y, self.explosion_images, 20, 4, True)
            
            self.health = 99999          # Prevent multiple destructions
            self.kill()                  # Remove explosive crate from the game

