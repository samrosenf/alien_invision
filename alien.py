import os.path

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game, level=1):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Setup life and lives of the alien
        self.x, self.y = 0, 0
        self.level = level
        self.life = level

        # Load image according to the alien level
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
        # Load the alien image and set its rect attritbute.
        self.image = pygame.image.load(self._get_image_path()).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def _get_image_path(self):
        """Load the right image depnded on the current level."""
        image_color_dict = {
            1: 'teal',
            2: 'green',
            3: 'purple',
            4: 'blue',
            5: 'grey',
            6: 'orange',
            7: 'yellow',
            8: 'pink',
            9: 'red',
        }
        alien_color = image_color_dict.get(
            self.life, 'red')  # if level don't exist use red
        image_file_name = alien_color + '_alien_ship.png'
        return os.path.join('images', image_file_name)
