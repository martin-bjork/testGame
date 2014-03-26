from __future__ import division
from math import pi

import pygame
import pymunk

import scene
import collision_callbacks as col_call

# TODO: Add more classes, such as wall


class Shape(pygame.sprite.Sprite):
    '''An abstract base class for all other shapes in the game'''
    # TODO: Make abstract for real? With the abc module?

    # Set a base collision type for all objects
    collision_type = col_call.BASE_TYPE

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Pymunk properties
        self._body = None
        self._shape = None
        self._friction = 1.0
        self._elasticity = 0.5

        # Pygame properties
        self._baseimage = None
        self.image = None
        self.rect = None
        self._color = None

    # Getters/Setters

    def get_body(self):
        return self._body

    def get_shape(self):
        return self._shape

    def get_friction(self):
        return self._friction

    def get_elasticity(self):
        return self._elasticity

    def get_baseimage(self):
        return self._baseimage

    def set_baseimage(self, image):
        self._baseimage = image

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color


# NOTE: Needed? Maybe remove? If there is not any more
# functionality we want to add here.
class StaticShape(Shape):
    '''An abstract base class for all static shapes in the game'''
    # TODO: Make abstract for real? With the abc module?

    # The collision type for static objects
    collision_type = col_call.STATIC_TYPE

    def __init__(self):
        super(StaticShape, self).__init__()

        # Pymunk properties
        self._body = pymunk.Body()


class MovingShape(Shape):
    '''An abstract base class for all moving objects in the game'''
    # TODO: Make abstract for real? With the abc module?

    # The base collision type for moving objects
    collision_type = col_call.MOVING_TYPE

    def __init__(self):
        super(MovingShape, self).__init__()

    def update(self, game):
        '''Updates the position of the sprite to match the Pymunk shape'''
        # NOTE: This will throw an exception if image, rect etc
        # are not initialized; Make sure all classes that inherit from this
        # class initializes all variables correctly
        self.image = pygame.transform.rotate(self._baseimage,
                                             self._body.angle*180/pi)
        self.rect = self.image.get_rect()
        self.rect.center = scene.pymunk_to_pygame_coords(
            self._body.position[0], self._body.position[1],
            game.get_screen_size()[1])


class Rectangle(MovingShape):
    '''A class for rectangles'''

    def __init__(self, space, width=50, height=50, mass=1,
                 position=(100, 100), color=(0, 0, 0)):
        super(Rectangle, self).__init__()

        # Pymunk properties
        points = [(-width/2, -height/2), (width/2, -height/2),
                  (width/2, height/2), (-width/2, height/2)]
        inertia = pymunk.moment_for_box(mass, width, height)
        self._body = pymunk.Body(mass, inertia)
        self._shape = pymunk.Poly(self._body, points)
        self._body.position = position

        space.add(self._body, self._shape)

        self._shape.collision_type = Rectangle.collision_type

        # A hack to be able to access the object via it's shape
        self._shape.__setattr__('obj', self)

        # Pygame properties
        self._color = color
        self._baseimage = pygame.Surface((width, height))
        self._baseimage.fill((self._color))
        self.image = self._baseimage
        self.rect = self.image.get_rect()
