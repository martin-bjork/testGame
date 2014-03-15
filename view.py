import os

import pygame

WIDTH = 800
HEIGHT = 800


def set_up_window():
    pygame.init()

    # Initialize the display
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    # Decorate window, hide cursor
    icon = load_image('smiley_small.png')
    pygame.display.set_caption('Test window')
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(0)

    # TODO: Add more stuff here

    # Load background image
    background_image = load_image('smiley.png')
    screen.blit(background_image, (0, 0))

    # Draw window
    pygame.display.flip()


def load_image(file_name):
    "loads an image, prepares it for play"
    full_name = os.path.join('images', file_name)
    try:
        surface = pygame.image.load(full_name)
    except pygame.error:
        print 'Could not load image "{name}".\nError message: {message}'\
            .format(name=file_name, message=pygame.get_error())
        raise SystemExit
    return surface.convert()
