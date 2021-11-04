import random
import os.path
import pygame
from pygame.sprite import Sprite


class Powerup(Sprite):
    """A class for upgrades being dropped from the top."""

    def __init__(self, ai_game, imagepath):
        """Initialize the drop and its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load(imagepath).convert_alpha()
        self.rect = self.image.get_rect()
        x_start = self.rect.width
        x_end = self.screen_rect.width - self.rect.width
        self.x = random.randint(x_start, x_end)
        self.y = self.rect.height
        self.rect.x, self.rect.y = self.x, self.y

    def update(self):
        """Update the power up location"""
        self.y += self.settings.powerup_speed
        self.rect.y = self.y


class LifePowerUp(Powerup):
    """A class for life powerup."""

    def __init__(self, ai_game):
        imagepath = os.path.join('images', 'heart.png')
        super().__init__(ai_game, imagepath)


class WeaponPowerUp(Powerup):
    """A class for weapon powerup."""

    def __init__(self, ai_game):
        imagepath = os.path.join('images', 'weapon.png')  # TODO
        super().__init__(ai_game, imagepath)


class ShieldPowerUp(Powerup):
    """A class for sheild powerup."""

    def __init__(self, ai_game):
        imagepath = os.path.join('images', 'shield.png')  # TODO
        super().__init__(ai_game, imagepath)
