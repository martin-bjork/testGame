import os

import pygame

# TODO: Add exception handling


class Music():
    '''
    A wrapper for pygame.mixer.music to be able to check which music file
    is currently being played.
    '''

    def __init__(self):
        self._currently_loaded = None

    def load(self, file_name):
        '''
        Load the file named "file_name".

        Input:
            * file_name: String
                - The name of the file that is to be loaded.
        '''

        base_dir = os.path.join('Data', 'sound')
        full_name = os.path.join(base_dir, file_name)

        pygame.mixer.music.load(full_name)
        self._currently_loaded = file_name

    def play(self, reps=-1):
        '''
        Play the currently loaded file.

        Input:
            * reps: Int
                - The number of times the sond is to be repeated.
                  0 -> play once, don't repeat; 1 -> play once, repeat once etc
                  -1 -> repeat indefinitely.
                - Default: -1
        '''

        pygame.mixer.music.play(reps)

    def set_volume(self, vol):
        '''
        Set the volume of the music.

        Input:
            * vol: Float 0.0 - 1.0
                - The volume to be set.
        '''
        pygame.mixer.music.set_volume(vol)

    def load_and_play(self, file_path, reps=-1):
        '''
        Load the file found at "file_path" and start playing it.

        Input:
            * file_path: String
                - The path to the file that is to be loaded.
            * reps: Int
                - The number of times the sond is to be repeated.
                  0 -> play once, don't repeat; 1 -> play once, repeat once etc
                  -1 -> repeat indefinitely.
                - Default: -1
        '''

        self.load(file_path)
        self.play(reps)

    def get_playing(self):
        '''
        Checks which song is currently loaded and whether it is playing.

        Output:
            * currently_loaded: String
                - The path of the file that is currently loaded.
            * playing: Bool
                - Whether or not the currently loaded file is playing.
        '''
        return self._currently_loaded, pygame.mixer.music.get_busy()
