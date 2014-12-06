from __future__ import division

import pygame


class Camera():
    '''
    A class that handles the viewing of the world.
    It takes care of conversion between wolrd and screen coordinates,
    makes sure the correct part of the world is being displayed and
    handles the updating of the screen.
    '''

    def __init__(self, pos=(1.0, 1.0), zoom=1.0, margin=1.0):
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
            * margin: Float
                - The 'margin of the screen', i.e. when the player is margin
                  world units from the edge of the screen, the camera starts
                  moving to keep the player on screen.
                - Default: 1.0
        '''

        self._pos = pos
        self._zoom = zoom
        self._margin = 1.0
        info = pygame.display.Info()
        width = info.current_w / zoom
        height = info.current_h
        self._size = (width, height)

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

    def move(self, vec):
        '''
        Moves the camera - adds vec to the current position.
        '''

        self._pos = tuple(a + b for a, b in zip(self._pos, vec))

    def update(self, game):
        '''
        Updates the camera object and displays the world.
        '''

        sprite_group = game.get_sprite_group()
        screen = pygame.display.get_surface()
        background = game.get_background()
        screen_rect = screen.get_rect(center=self.
                                      world_to_screen_coords(self._pos))
        player = game.get_player()
        player_pos = player.get_pos()

        # Move the camera to the players position
        # TODO: Make sure the camera doesn't move beyond the edge of the world
        # TODO: Add smooth camera movements.
        dist = [0, 0]
        if player_pos[0] < self._pos[0] + self._margin:
            # The player is too far to the left
            dist[0] = player_pos[0] - (self._pos[0] + self._margin)
        elif player_pos[0] < self._pos[0] + self._size[0] - self._margin:
            # The player is too far to the right
            dist[0] = player_pos[0] - (self._pos[0] + self._size[0]
                                       - self._margin)
        if player_pos[1] < self._pos[1] + self._margin:
            # The player is too far down
            dist[1] = player_pos[1] - (self._pos[1] + self._margin)
        elif player_pos[1] < self._pos[1] + self._size[1] - self._margin:
            # The player is too far up
            dist[1] = player_pos[1] - (self._pos[1] + self._size[1]
                                       + self._margin)

        self.move(dist)

        # Blit all objects to the background
        # TODO: Check if this can be optimized
        # TODO: Clear the sprites from last frame
        for sprite in sprite_group:
            # Make sure it actually is on screen before blitting
            if screen_rect.colliderect(sprite.rect):
                background.blit(sprite.image, sprite.rect)

        # Blit the background to the screen
        w, h = self.world_to_screen_coords(self._pos)
        screen.blit(background, (-w, -h))

    # Getters/setters

    def get_pos(self):
        return self._pos

    def get_zoom(self):
        return self._zoom

    def get_margin(self):
        return self._margin

    def get_size(self):
        return self._size
