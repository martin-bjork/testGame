# Conversion functions between pygame and pymunk coordinates.

# TODO: Make the connection between pygame and pymunk coordinates looser
#       so it's possible to have a moving camera to view the world.
# TODO: Use pos tuple instead of x and y ints.

import pygame


def pymunk_to_pygame_coords(x, y):
    '''
    A function to convert from pymunk to pygame coordintes.

    Input:
        * x: Float
            - The x-coordinate in pymunk.
        * y: Float
            - The y-coordinate in pymunk.
    Output:
        * pos: 2-tuple of ints
            - The pygame coordinates corresponding to the input.
    '''

    return int(x), int(pygame.display.Info().current_h - y)


def pygame_to_pymunk_coords(x, y):
    '''
    A function to convert from pygame to pymunk coordintes.

    Input:
        * x: Int
            - The x-coordinate in pygame.
        * y: Int
            - The y-coordinate in pygame.
    Output:
        * pos: 2-tuple of ints
            - The pymunk coordinates corresponding to the input.
    '''

    return x, -y - pygame.display.Info().current_h
