import os
import pygame


def load_sound(file_name):

    if not pygame.mixer:
        print 'Warning: Unable to load module pygame.mixer'
        return DummySound()

    fullname = os.path.join('sound', 'sound_data', file_name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Pygame error: ', message
        print 'Cannot load sound:', file_name
        return DummySound()
    return sound


class DummySound:
    def play(self):
        pass

    def set_volume(self, level):
        pass
