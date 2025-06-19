import pygame
import toolbox
import math
import random
from explosion import Explosion
from powerup import PowerUp

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.containers)  # Initialize sprite and add to groups
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player  # Reference to player for targeting

        # Load different enemy images for variety
        self.image = pygame.image.load("assets/Enemy_05.png")
        self.image1 = pygame.image.load("assets/Enemy_02.png")
        self.image2 = pygame.image.load("assets/Enemy_03.png")
        self.image3 = pygame.image.load("assets/Enemy_04.png")

        # Load explosion images for when enemy dies
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("assets/MediumExplosion1.png"))
        self.explosion_images.append(pygame.image.load("assets/MediumExplosion2.png"))
        self.explosion_images.append(pygame.image.load("assets/MediumExplosion3.png"))

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.angle = 0           # Direction enemy is facing (in degrees)
        self.speed = 0.5         # Movement speed
        self.health_max = 20
        self.health = self.health_max         # Enemy health points
        self.hurt_timer = 0      # Timer for hit animations or effects (not shown here)
        self.damage = 1          # Damage dealt to player or objects on collision
        self.obstale_anger = 0   # Counter for how angry enemy gets when blocked by crates
        self.obstale_anger_max = 100  # Threshold to deal damage to crates
        self.powerup_drop_chance = 50 # Percent chance to drop power-up on death

        # Randomly select one of the enemy images for appearance variety
        enemy_type = random.randint(0, 3)
        if enemy_type == 0:
            self.image = self.image
        elif enemy_type == 1:
            self.image = self.image1
        elif enemy_type == 2:
            self.image = self.image2
        elif enemy_type == 3:
            self.image = self.image3

        self.sfx_explode = pygame.mixer.Sound("assets/sfx/explosion-small.wav")  # Sound effect on death

    def update(self, projectiles, crates, explosions):
        # Calculate angle to face the player
        self.angle = toolbox.angleBetweenPoints(self.x, self.y, self.player.x, self.player.y)
        angle_rads = math.radians(self.angle)

        # Calculate movement based on angle and speed
        self.x_move = math.cos(angle_rads) * self.speed
        self.y_move = -math.sin(angle_rads) * self.speed

        # Create a test rectangle to check collisions before moving
        test_rect = self.rect
        new_x = self.x + self.x_move
        new_y = self.y + self.y_move

        # Check horizontal collisions with crates
        test_rect.center = (new_x, self.y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_x = self.x      # Cancel horizontal movement if blocked
                self.getAngry(crate)  # Increase anger and potentially damage crate

        # Check vertical collisions with crates
        test_rect.center = (self.x, new_y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_y = self.y      # Cancel vertical movement if blocked
                self.getAngry(crate)

        # Update position
        self.x = new_x
        self.y = new_y
        self.rect.center = (self.x, self.y)

        # Check for collisions with projectiles (like water balloons)
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.getHit(projectile.damage)  # Take damage
                projectile.explode()             # Trigger projectile explosion

        # Check for damage from explosions (e.g. crates exploding)
        for explosion in explosions:
            if explosion.damage:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)

        # Draw the enemy rotated towards player
        image_to_draw, image_rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.screen.blit(image_to_draw, image_rect)

    def getHit(self, damage):
        # Knockback effect when hit
        self.x -= self.x_move * 15
        self.y -= self.y_move * 15

        # Reduce health by damage taken
        self.health -= damage

        # Check if enemy is dead
        if self.health <= 0:
            self.health = 99999  # Prevent multiple kills
            self.sfx_explode.play()
            self.player.getScore(50)  # Increase player's score on kill

            # Create explosion effect at enemy's position
            Explosion(self.screen, self.x, self.y, self.explosion_images, 20, 0, False)

            # Random chance to drop a power-up
            if random.randint(0, 100) < self.powerup_drop_chance:
                PowerUp(self.screen, self.x, self.y)

            self.kill()  # Remove enemy from all groups

    def getAngry(self, crate):
        # Increase anger when blocked by a crate
        self.obstale_anger += 1

        # When anger maxes out, damage the crate and reset anger
        if self.obstale_anger >= self.obstale_anger_max:
            crate.getHit(self.damage)
            self.obstale_anger = 0  # Reset anger counter


# Boss enemy class inherits from Enemy but stronger and faster
class Boss(Enemy):
    def __init__(self, screen, x, y, player):
        Enemy.__init__(self, screen, x, y, player)  # Initialize as a normal enemy first
        
        # Load boss-specific image (placeholder path, update as needed)
        self.image = pygame.image.load("assets/TopView_Robot_Asset_Pack/EnemyId_150071_red.png")
        
        self.health_max = 100    # Boss has more health than normal enemies
        self.health = self.health_max
        self.speed = 0.75    # Boss moves faster
        self.damage = 2      # Boss deals more damage

        self.health_bar_width = 64# self.image.get_width()  # Health bar is as wide as the image
        self.health_bar_height = 8                     # Fixed height for health bar
        self.health_bar_green = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)  # Green part
        self.health_bar_red = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)    # Red background
    
    def update(self, projectiles, crates, explosions):
        # Calculate angle to face the player
        self.angle = toolbox.angleBetweenPoints(self.x, self.y, self.player.x, self.player.y)
        angle_rads = math.radians(self.angle)

        # Calculate movement based on angle and speed
        self.x_move = math.cos(angle_rads) * self.speed
        self.y_move = -math.sin(angle_rads) * self.speed

        # Create a test rectangle to check collisions before moving
        test_rect = self.rect
        new_x = self.x + self.x_move
        new_y = self.y + self.y_move

        # Check horizontal collisions with crates
        test_rect.center = (new_x, self.y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_x = self.x      # Cancel horizontal movement if blocked
                self.getAngry(crate)  # Increase anger and potentially damage crate

        # Check vertical collisions with crates
        test_rect.center = (self.x, new_y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_y = self.y      # Cancel vertical movement if blocked
                self.getAngry(crate)

        # Update position
        self.x = new_x
        self.y = new_y
        self.rect.center = (self.x, self.y)

        # Check for collisions with projectiles (like water balloons)
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.getHit(projectile.damage)  # Take damage
                projectile.explode()             # Trigger projectile explosion

        # Check for damage from explosions (e.g. crates exploding)
        for explosion in explosions:
            if explosion.damage:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)

        # Draw the enemy rotated towards player
        image_to_draw, image_rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.screen.blit(image_to_draw, image_rect)

        self.health_bar_red.x = self.rect.x
        self.health_bar_red.bottom = self.rect.y - 5
        pygame.draw.rect(self.screen, (255, 0, 0 ), self.health_bar_red)
        self.health_bar_green.topleft = self.health_bar_red.topleft
        health_percentage = self.health / self.health_max
        self.health_bar_green.width = self.health_bar_width * health_percentage
        pygame.draw.rect(self.screen, (0, 255,0), self.health_bar_green)
