import os

import pygame

WIDTH = 600
HEIGHT = 480


def init_window():
    '''Initializes a pygame window, sets caption, icon and background.
    Returns the pygame display surface.'''
    pygame.init()

    # Initialize the display
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    # Decorate window, hide cursor
    icon = load_image('smiley_small.png')
    pygame.display.set_caption('Test window')
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(0)

    # TODO: Add more stuff here

    # Create background
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((200, 200, 200))    # TODO: Choose a better color
    screen.blit(background, (0, 0))

    # Draw window
    pygame.display.flip()

    return screen, background


def load_image(file_name):
    '''Loads an image into pygame. The image is found in the directory "images"
    and has the file name "file_name". Returns a pygame Surface object.'''
    full_name = os.path.join('images', file_name)
    try:
        surface = pygame.image.load(full_name)
    except pygame.error:
        print 'Could not load image "{name}".\nError message: {message}'\
            .format(name=file_name, message=pygame.get_error())
        raise SystemExit
    return surface.convert_alpha()
