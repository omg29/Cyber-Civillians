import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, images, duration, damage, damage_player):
        """
        Initialize an animated explosion effect.

        Args:
            screen: The pygame display surface to draw on.
            x, y: Coordinates where the explosion occurs.
            images: List of images for the explosion animation frames.
            duration: How long each frame lasts (in update cycles).
            damage: Amount of damage explosion does to enemies (or objects).
            damage_player: Boolean, whether explosion damages the player.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.images = images              # Frames of the explosion animation
        self.duration = duration          # Duration each frame stays visible
        self.damage = damage
        self.damage_player = damage_player
        
        # Use the size of the first image for the rect and center it at (x, y)
        self.rect = self.images[0].get_rect()
        self.rect.center = (self.x, self.y)
        
        self.animation_timer = duration  # Timer counting down for current frame
        self.frame_to_draw = 0            # Current frame index
        self.last_frame = len(images) - 1  # Last frame index
    
    def update(self):
        """
        Update explosion animation each game cycle.

        - Decreases the timer counting down the current frame.
        - When timer reaches zero, move to next frame or kill sprite if finished.
        - Draw current frame of explosion on the screen.
        """
        self.animation_timer -= 1
        
        # Time to switch to next frame?
        if self.animation_timer <= 0:
            if self.frame_to_draw < self.last_frame:
                self.frame_to_draw += 1         # Move to next frame
                self.animation_timer = self.duration  # Reset timer for next frame
            else:
                self.kill()                    # Animation done, remove sprite
        
        # Draw the current frame on the screen at the explosion position
        self.screen.blit(self.images[self.frame_to_draw], self.rect)

