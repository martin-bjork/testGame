import os

import pygame

from sound import music

WIDTH = 600
HEIGHT = 480


def init_window():
    '''Initializes a pygame window, sets caption, icon and background.
    Returns the pygame display surface.'''

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
    screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)

    # Decorate window, hide cursor
    # NOTE: Unnecessary if we use pygame.NOFRAME
    icon = load_image('smiley_small.png')
    pygame.display.set_caption('Test window')
    pygame.display.set_icon(icon)

    # TODO: Add more stuff here (?)

    # Create background
    background = pygame.Surface((WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    # Draw window
    pygame.display.flip()

    return screen, background


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


def load_and_scale(file_name, scale):
    '''
    Loads the image named file_name and scales it to the
    size specified by scale.

    Input:
        * file_name: String
            - The file name of the image that is to be loaded.
        * scale: 2-Tuple of ints
            - The wanted size of the image in pixels (width, height).
    Output:
        * surface: pygame.Surface
            - A pygame Surface containing the image.
    '''

    return pygame.transform.smoothscale(load_image(file_name), scale)
