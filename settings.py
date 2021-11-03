import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800

        # Game settings
        self.FPS = 60

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (224, 222, 58)
        self.bullets_allowed = 10

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Highscore file
        self.highscore_file = 'highscore.txt'

        self.initialize_dynamic_settings()

    def load_bg(self):
        self.bg = pygame.image.load("images/space_bg.jpg").convert()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throghout the game."""
        self.ship_speed = 5.0
        self.bullet_speed = 3.0
        self.alien_speed = 2.5

        # fleet_direction of 1 represnts right; -1 represnts left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
