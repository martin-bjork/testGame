import os
import pygame


def load_sound(file_name):

    if not pygame.mixer:
        print 'Warning: Unable to load module pygame.mixer'
        return dummy_sound()

    fullname = os.path.join('sound/sound_data', file_name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Pygame error: ', message
        print 'Cannot load sound:', file_name
        return dummy_sound()
    return sound


class dummy_sound:
    def play(self):
        pass
