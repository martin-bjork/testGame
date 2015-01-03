from __future__ import division

import pygame
import yaml


class Camera(yaml.YAMLObject):
    '''
    A class that handles the viewing of the world.
    It takes care of conversion between wolrd and screen coordinates,
    makes sure the correct part of the world is being displayed and
    handles the updating of the screen.
    '''

    yaml_tag = '!Camera'

    def __init__(self, pos=(0.0, 0.0), zoom=1.0, world_size=(600, 480),
                 margin=100):
        '''
        Constructor for the Camera object.

        Input:
            * pos: 2-tuple of floats
                - The position of the upper left corner of the camera
                  relative to the upper left corner of the background
                  in screen coordinates.
                - Default: (0.0, 0.0)
            * zoom: Float
                - The conversion factor between world and screen coordinates.
                  1 world unit = zoom screen units; i.e. the scale is 1:zoom.
                - Default: 1.0
        '''

        self._pos = pos
        self._zoom = zoom
        self._world_size = world_size
        self._margin = margin
        screen = pygame.display.get_surface()
        self._size = screen.get_size()
        self._screenrect = screen.get_rect()
        self._screenrect.center = (self._size[0]/2, self._size[1]/2)

    @classmethod
    def from_yaml(cls, loader, node):
        '''
        A constructor that YAML uses to create instances of this class.
        '''

        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        pos = values['pos']
        zoom = values['zoom']
        world_size = values['world_size']
        margin = values['margin']

        # Return an instance of the object
        return cls(pos=pos, zoom=zoom, world_size=world_size, margin=margin)

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''
        A method used by YAML to represent an instance of this class.
        '''

        # Construct a dict containing only the properties (wrong word...)
        # we want to use in the representation

        mapping = {'pos': instance._pos,
                   'zoom': instance._zoom,
                   'world_size': instance._world_size,
                   'margin': instance._margin}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)

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

        w = int(x * self._zoom - self._pos[0])
        h = int(self._world_size[1] - self._pos[1] - y)

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

        x = (w + self._pos[0]) / self._zoom
        y = (h + self._pos[1] - self._world_size[1]) / self._zoom

        return x, y

    def move(self, vec):
        '''
        Moves the camera the distance specified in vec
        '''

        self._pos = tuple(a + b for a, b in zip(self._pos, vec))

    def update(self, game):
        '''
        Updates the camera object to view the player,
        draws everything to the screen and flips the screen.
        '''
        # FIXME: When moving very fast, the camera moves slightly past
        #        the edge of the world - this must be fixed.

        sprite_group = game.get_sprite_group()
        screen = pygame.display.get_surface()
        background = game.get_background()
        player_obj = game.get_player().get_object()

        # Calculate the position of the player relative to
        # the center of the screen
        rel_pos = [a - b for a, b in zip(player_obj.rect.center,
                                         screen.get_rect().center)]
        diff = [0, 0]

        # Calculate how far the camera must move to
        # make sure the player is on-screen
        if rel_pos[0] > self._size[0]/2 - self._margin:
            # The player is too far to the right
            diff[0] = rel_pos[0] - (self._size[0]/2 - self._margin)
        elif rel_pos[0] < -(self._size[0]/2 - self._margin):
            # The player is too far to the left
            diff[0] = rel_pos[0] + (self._size[0]/2 - self._margin)

        if rel_pos[1] > self._size[1]/2 - self._margin:
            # The player is too far down
            diff[1] = rel_pos[1] - (self._size[1]/2 - self._margin)
        elif rel_pos[1] < -(self._size[1]/2 - self._margin):
            # The player is too far up
            diff[1] = rel_pos[1] + (self._size[1]/2 - self._margin)

        # Make sure the camera doesn't move past the edge of the world
        if diff[0] > 0 and self._pos[0] + self._size[0] >= \
                self._world_size[0]:
            # Camera wants to move to the right but has reached the right
            # edge of the world; don't move to the right
            diff[0] = 0
        elif diff[0] < 0 and self._pos[0] <= 0:
            # Camera wants to move to the left but has reached the left
            # edge of the world; don't move to the left
            diff[0] = 0

        if diff[1] > 0 and self._pos[1] + self._size[1] >= \
                self._world_size[1]:
            # Camera wants to move down but has reached the lower
            # edge of the world; don't move down
            diff[1] = 0
        elif diff[1] < 0 and self._pos[1] <= 0:
            # Camera wants to move up but has reached the upper
            # edge of the world; don't move up
            diff[1] = 0

        # Move the camera to the new position
        self.move(diff)

        # Clear the screen
        screen.blit(background, (-self._pos[0], -self._pos[1]))

        # Blit everything to the screen
        for sprite in sprite_group:
            screen.blit(sprite.image, sprite.rect)

        # Flip the display
        pygame.display.flip()
