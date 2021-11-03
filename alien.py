import os.path

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.x, self.y = 0, 0

        # Load image according to the alien level
        self.life = self.stats.alien_level
        self.load_image()

    def update(self):
        """Move the alien to the right."""
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        """Return True if alien is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def load_image(self):
        """Load the right image depnded on the current level."""
        image_color_dict = {
            1: 'teal',
            2: 'green',
            3: 'purple',
            4: 'orange'
        }

        # Load the alien image and set its rect attritbute.
        alien_color = image_color_dict.get(self.life, 'orange') # if level don't exist use orange
        image_path = self._get_image_path(alien_color)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def _get_image_path(self, color):
        image_file_name = color + '_alien_ship.png'
        return os.path.join('images', image_file_name)
