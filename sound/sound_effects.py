# Functions for handling sound

import os
import pygame


def load_sound(file_name):
    '''
    Loads the sound file named "file_name".
    If the file for some reason cannot be loaded it returns
    a dummy sound that does nothing at all but behaves like a sound object.
    '''

    # Check if the pygame mixer has been loaded.
    # If not, return dummy sound object.
    if not pygame.mixer:
        print 'Warning: Unable to load module pygame.mixer'
        return DummySound()

    # Get the full path to the sound file.
    base_dir = os.path.join('Data', 'sound')
    fullname = os.path.join(base_dir, file_name)

    # Try to load the sound file. If an error occurs, print the error
    # and return a dummy sound object.
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Pygame error: ', message
        print 'Cannot load sound:', file_name
        return DummySound()
    return sound


class DummySound:
    '''
    A dummy sound object, is returned if a real sound couldn't be loaded.
    '''

    def play(self):
        pass

    def set_volume(self, level):
        pass
