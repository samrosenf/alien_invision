import pygame.mixer
import pygame.mixer_music

class Sound:
    """A class for all the sound in the game."""
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/bg_music.ogg')
        pygame.mixer.music.play()
        # print(pygame.mixer.music.get_volume())
        pygame.mixer.music.set_volume(0.5)