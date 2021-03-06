import pygame
import random


class Event:
    """This is a class for custom event."""

    def __init__(self, id):
        self.id = pygame.USEREVENT + id

    def set_timer(self, base_time, random_time):
        event_time = base_time + random.randint(-random_time, random_time)
        pygame.time.set_timer(self.id, event_time)


class Events:
    """This is a class for all the custom events in the game."""

    def __init__(self, ai_game):
        self.settings = ai_game.settings

        self.enemy_shooting = Event(self.settings.enemy_shooting_id)
        self.enemy_shooting.set_timer(
            self.settings.bullet_gen_time, self.settings.bullet_rand_gen_time)

        self.powerup_drop = Event(self.settings.powerup_id)
        self.powerup_drop.set_timer(
            self.settings.powerup_gen_time, self.settings.powerup_rand_gen_time)
