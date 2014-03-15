import pygame

WIDTH = 600
HEIGHT = 480


def set_up_window():
    pygame.init()

    # Initialize the display
    winstyle = 0            # FULLSCREEN
    best_color_depth = pygame.display.mode_ok([WIDTH, HEIGHT], winstyle, 32)
    screen = pygame.display.set_mode([WIDTH, HEIGHT], winstyle,
                                     best_color_depth)

    # Hide cursor
    pygame.display.set_caption('Test window')
    pygame.mouse.set_visible(0)

    # TODO: Add more stuff here (set up background etc)
