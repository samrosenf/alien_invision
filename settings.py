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
        self.MAX_LEVEL = 20

        # Ship settings
        self.ship_limit = 3
        self.max_ships = 6

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15

        # Player bullet settings
        self.player_bullet_color = (224, 222, 58)
        self.bullets_allowed = 10

        # Enemy bullet settings
        self.enemy_bullet_color = (255, 0, 0)

        # Enemy settings
        self.fleet_y_start = 90
        self.fleet_drop_speed = 10

        # Events IDs
        self.enemy_shooting_id = 1
        self.powerup_id = 2


        # Event times
        self.bullet_gen_time = 2000  # in ms
        self.bullet_rand_gen_time = 200  # in ms
        self.powerup_gen_time = int(4E4)  # in ms
        self.powerup_rand_gen_time = int(1E1)  # in ms

        # Powerup settings
        self.powerup_speed = 1.1

        # How quickly the game speeds up
        self.speedup_scale = 1.2

        # How quickly the enemy point values increase
        self.score_scale = 1.5

        # Highscore file
        self.highscore_file = 'highscore.txt'

        self.initialize_dynamic_settings()

    def load_bg(self):
        self.bg = pygame.image.load("images/space_bg.jpg").convert()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throghout the game."""
        self.ship_speed = 5.0
        self.player_bullet_speed = 3.0
        self.enemy_speed = 2.5
        self.enemy_bullet_speed = 2.0

        # fleet_direction of 1 represnts right; -1 represnts left.
        self.fleet_direction = 1

        # Scoring
        self.hit_points = 20
        self.kill_points = 100

    def increase_speed(self):
        """Increase speed settings and enemy point values."""
        self.ship_speed *= self.speedup_scale
        self.player_bullet_speed *= self.speedup_scale
        self.enemy_bullet_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)
