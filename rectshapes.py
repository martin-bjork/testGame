from __future__ import division

import pygame
import pymunk

import scene


class RectShape(pygame.sprite.Sprite):

    def __init__(self, game):
        # TODO: Clean up this mess...
        pygame.sprite.Sprite.__init__(self)
        self._keys = {}

        width, height = game.get_screen_size()

        # TODO: Currently uses a radius, should change such that any length of side is possible
        radius = 50
        mass = 1
        inertia = pymunk.inf      # No rotation
        box_points = [(-radius/2, -radius/2), (radius/2, -radius/2),
                                    (radius/2, radius/2), (-radius/2, radius/2)]
        self._body = pymunk.Body(mass, inertia)
        self._shape = pymunk.Poly(self._body, box_points, (0, 0))
        self._body.position = width - 180, radius + 20
        self._shape.friction = 1.0
        self._shape.elasticity = 0.5
        self._shape.collision_type = 1

        self._shape.ignore_draw = False
        space = game.get_space()
        space.add(self._body, self._shape)

        self._baseimage = pygame.Surface((radius, radius))
        self.image = self._baseimage
        self.rect_width = radius
        self.rect_height = radius
        #self.rect = pygame.Rect((0, 0, self.rect_width, self.rect_height))
        self.rect = self.image.get_rect()
        print "created Rectangle"

    def update(self):
        '''Updates the position of the sprite to match
        the position of it's body.'''
        # self.image = pygame.transform.rotate(self._baseimage,
        #                                      self._body.angle*180/pi)
        self.rect_width = self._baseimage.get_width()
        self.rect_height = self._baseimage.get_height()
        #self.rect = pygame.Rect((0, 0, self.rect_width, self.rect_height))
        self.image.get_rect()
        self.rect.center = scene.pymunk_to_pygame_coords(self._body.position[0],
                                                         self._body.position[1],
                                                         480)

    # Getters/setters

    def get_keys(self):
        return self._keys

    def get_body(self):
        return self._body

    def get_shape(self):
        return self._shape

    def getimage(self):
        return self.image

    def get_acceleration(self):
        return self._acceleration
