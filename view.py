import os

import pygame

from sound import music

# TODO: Set this (and other things) via settings file
WIDTH = 600
HEIGHT = 480
FULLSCREEN = True


def init_window():
    '''Initializes a pygame window, sets caption, icon and background.
    Returns the pygame display surface.'''

    if not FULLSCREEN:
        # Set the position of the window on the screen
        # (must be called before pygame.init())
        # FIXME: Apparently, this causes the program to crash on Mac.
        #        Check why and fix.
        pos = (500, 300)
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(pos[0]) + "," + str(pos[1])

    # Setup mixer to avoid sound lag (must be done before initializing pygame)
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()

    # A hack to add a "home made" music player to pygame in order to be able
    # to access the name of the sound that is currently playing.
    pygame.__setattr__('music_player', music.Music())

    # Initialize the display
    if FULLSCREEN:
        pygame.display\
            .set_mode([0, 0],
                      pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    else:
        pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)


def load_image(file_name):
    '''
    Loads the image named file_name.

    Input:
        * file_name: String
            - The file name of the image that is to be loaded.
    Output:
        * surface: pygame.Surface
            - A pygame Surface containing the image.
    '''

    full_name = os.path.join('images', file_name)

    try:
        surface = pygame.image.load(full_name)
    except pygame.error:
        print 'Could not load image "{name}".\nError message: {message}'\
            .format(name=file_name, message=pygame.get_error())
        raise SystemExit

    return surface.convert_alpha()


def load_and_scale(file_name, size):
    '''
    Loads the image named file_name and scales it to the
    size specified by scale.

    Input:
        * file_name: String
            - The file name of the image that is to be loaded.
        * size: 2-Tuple of ints
            - The wanted size of the image in pixels (width, height).
    Output:
        * surface: pygame.Surface
            - A pygame Surface containing the image.
    '''

    return pygame.transform.smoothscale(load_image(file_name), size)
