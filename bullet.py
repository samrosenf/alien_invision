import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        

        # Create a bullet rect at (0,0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.mask = pygame.mask.Mask(self.rect.size)
        self.mask.fill()

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)


class PlayerBullet(Bullet):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.color = self.settings.player_bullet_color
        # Put the bullet so it's coming out the Player ship.
        self.rect.midtop = ai_game.ship.rect.midtop
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.player_bullet_speed
        # Update the rect position.
        self.rect.y = self.y

class EnemyBullet(Bullet):
    def __init__(self, ai_game, alien):
        super().__init__(ai_game)
        self.color = self.settings.enemy_bullet_color
        # Put the bullet so it's coming out the Enemy ship.
        self.rect.midbottom = alien.rect.midbottom
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y += self.settings.enemy_bullet_speed
        # Update the rect position.
        self.rect.y = self.y