from __future__ import division

import pygame


class Camera():
    '''
    A class that handles the viewing of the world.
    It takes care of conversion between wolrd and screen coordinates,
    makes sure the correct part of the world is being displayed and
    handles the updating of the screen.
    '''

    def __init__(self, pos=(1.0, 1.0), zoom=1.0):
        '''
        Constructor for the Camera object.

        Input:
            * pos: 2-tuple of floats
                - The position of the upper left corner of
                  the screen in world coordinates.
                - Default: (1.0, 1.0)
            * zoom: Float
                - The conversion factor between world and screen coordinates.
                  1 world unit = zoom screen units; i.e. the scale is 1:zoom.
                - Default: 1.0
        '''

        self._pos = pos
        self._zoom = zoom

    def world_to_screen_coords(self, x, y):
        '''
        Converts from world to screen coordintes.

        Input:
            * x: Float
                - The world x-coordinate.
            * y: Float
                - The world y-coordinate.
        Output:
            * w: Int
                - The corresponding screen x-coordinate.
            * h: Int
                - The corresponding screen y-coordinate.
        '''

        w = int((x - self._pos[0]) * self._zoom)
        h = int((self._pos[1] - y) * self._zoom)

        return w, h

    def screen_to_world_coords(self, w, h):
        '''
        Converts from screen to world coordintes.

        Input:
            * w: Int
                - The screen x-coordinate.
            * y: Int
                - The screen y-coordinate.
        Output:
            * x: Float
                - The corresponding world x-coordinate.
            * y: Float
                - The corresponding world y-coordinate.
        '''

        x = self._pos[0] + w / self._zoom
        y = self._pos[1] - h / self._zoom

        return x, y

    def update(self, game):
        '''
        Updates the camera object to view the player,
        draws everything to the screen and flips the screen.
        '''

        sprite_group = game.get_sprite_group()
        screen = pygame.display.get_surface()
        background = game.get_background()

        # Clear the screen
        screen.blit(background, (0, 0))

        # Blit everything to the screen
        for sprite in sprite_group:
            screen.blit(sprite.image, sprite.rect)

        # Flip the display
        pygame.display.flip()
