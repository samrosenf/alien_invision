import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and get its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.shield = False

        self.center_ship()

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def create_shield(self):
        old_rect_center = self.rect.center
        self.image = pygame.image.load('images/ship_shielded.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_center
        self.x = self.rect.x
        self.y = self.rect.y
        self.shield = True

    def remove_shield(self):
        old_rect_center = self.rect.center
        self.image = pygame.image.load('images/ship.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_center
        self.x = self.rect.x
        self.y = self.rect.y
        self.shield = False

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
