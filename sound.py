import pygame.mixer
import pygame.mixer_music


class Sound:
    """A class for all the sound in the game."""

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/bg_music1.ogg')
        # Play the music indefinately
        pygame.mixer.music.play(loops=-1)
        # print(pygame.mixer.music.get_volume())
        pygame.mixer.music.set_volume(0.3)

        # Loading sound effects
        self.boom_sound = pygame.mixer.Sound('sounds/explosion.wav')
        self.levelup_sound = pygame.mixer.Sound('sounds/levelup.wav')
        self.ship_hit_sound = pygame.mixer.Sound('sounds/shiphit.wav')

    def play_boom_sound(self):
        self.boom_sound.play()

    def play_levelup_sound(self):
        self.levelup_sound.play()

    def play_ship_hit_sound(self):
        self.ship_hit_sound.play()