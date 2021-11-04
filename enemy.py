import pygame
import os.path
from pygame.sprite import Sprite


class Enemy(Sprite):
    """A class to represent a single enemy in the fleet."""

    def __init__(self, ai_game, level=1):
        """Initialize the enemy and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self._load_enemy_images()

        # Setup life and lives of the enemy
        self.x, self.y = 0, 0
        self.level = level
        self.life = level

        # Load image according to the enemy level
        self.update_image()

    def drop_verticaly(self):
        self.y += self.settings.fleet_drop_speed

    def update(self):
        """Move the enemy to the right."""
        self.x += (self.settings.enemy_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        """Return True if enemy is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update_image(self):
        # Load the enemy image and set its rect attritbute.
        if self.life > len(self.images):
            image_idx = len(self.images) - 1
        else:
            image_idx = self.life - 1
        self.image = self.images[image_idx]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def _load_enemy_images(self):
        """Load all possible alien ship images"""
        self.images = []
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

        for i in range(1, 10):
            enemy_color = image_color_dict[i]
            image_file_name = enemy_color + '_enemy_ship.png'
            image_path = os.path.join('images', image_file_name)
            image = pygame.image.load(image_path).convert_alpha()
            self.images.append(image) 
