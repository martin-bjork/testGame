# Classes that represent objects in the game, such as moveable boxes,
# world boundaries, walls, etc.

from __future__ import division
from math import pi

import pygame
import pymunk
import yaml

import conversion
import collision_callbacks as col_call
import view

# TODO: Add properties such as friction and elasticity to the
# constructors instead of hard-coding.
# TODO: Improve the class descriptions.


class Shape(pygame.sprite.DirtySprite, yaml.YAMLObject):
    '''
    An abstract base class for all other shapes in the game.
    '''

    # TODO: Make abstract for real? With the abc module?

    # Set a base collision type for all objects
    collision_type = col_call.BASE_TYPE

    def __init__(self):
        '''
        Base constructor for all Shape objects and derivatives thereof.
        '''

        pygame.sprite.DirtySprite.__init__(self)

        # Pymunk properties
        self._body = None
        self._shape = None
        self._friction = 1.0
        self._elasticity = 0.5

        # Pygame properties
        self._baseimage = None
        self.image = None
        self.rect = None
        self.dirty = 1
        self._color = None

    def __repr__(self):
        # TODO: Make this better
        return str(self.__class__)

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


class StaticShape(Shape):
    '''
    An abstract base class for all static shapes in the game.
    '''

    # TODO: Make abstract for real? With the abc module?

    # The collision type for static objects
    collision_type = col_call.STATIC_TYPE

    def __init__(self, friction=1.0, elasticity=0.5):
        '''
        Base constructor for all static shapes in the game.

        Input:
            * friction: Float 0.0 - inf
                - The friction coefficient of the shape (the mu-factor).
                  Higher value -> more friction.
                - Default: 1.0
            * elasticity: Float 0.0 - 1.0
                - The elasticity of the shape.
                  Higher value -> "bouncier" collisions.
                  0.0 -> completely plastic collision -> no bounce.
                  1.0 -> completely elastic collision -> perfect bounce.
                - Default: 0.5
        '''
        Shape.__init__(self)

        # Pymunk properties
        self._body = pymunk.Body()
        self._friction = friction
        self._elasticity = elasticity


class MovingShape(Shape):
    '''
    An abstract base class for all moving objects in the game.
    '''

    # TODO: Make abstract for real? With the abc module?

    # The base collision type for moving objects
    collision_type = col_call.MOVING_TYPE

    def __init__(self):
        '''
        Base constructor for all moving shapes in the game.
        '''

        Shape.__init__(self)

    def update(self, game):
        '''
        Updates the position of the sprite to match the Pymunk shape.

        Input:
            * game: gameclass.Game
                - An object containing all info about the current game session.
        '''

        # NOTE: This will throw an exception if image, rect etc
        # are not initialized; Make sure all classes that inherit from this
        # class initializes all variables correctly

        # Rotate and scale the image
        self.image = pygame.transform.rotozoom(self._baseimage,
                                               self._body.angle*180/pi, 1)
        self.rect = self.image.get_rect()

        # Move the image to the right position
        self.rect.center = conversion.pymunk_to_pygame_coords(
            self._body.position[0], self._body.position[1],
            game.get_screen_size()[1])

        # TODO: Try to make this smarter; only set
        #       dirty to 1 if it has actually moved.
        self.dirty = 1

    def set_pos(self, pos):
        self._body.position = pos


class Rectangle(MovingShape):
    '''
    A class for rectangles.
    '''

    yaml_tag = '!Rectangle'

    def __init__(self, width=50, height=50, mass=1.0,
                 pos=(100, 100), color=(0, 0, 0),
                 image_file=None):
        '''
        Constructor for Rectangle.

        Input:
            * width: Int
                - The width of the rectangle.
                - Default: 50
            * height: Int
                - The height of the rectangle.
                - Default: 50
            * mass: Float
                - The mass of the rectangle.
                - Default: 1.0
            * position: 2-tuple of ints
                - The initial position of the rectangle.
                - Default: (100, 100)
            * color: 3-tuple of ints 0-255
                - The color of the rectangle in rgb.
                  If "image_file" is specified, "color" is ignored.
                - Default: (0, 0, 0)
            * image_file: String
                - The name of the file containing the image to be used
                  on the rectangle.
                  If set to None, the colour specified in "color"
                  is used instead.
                - Default: None
        '''

        MovingShape.__init__(self)

        self._width = width
        self._height = height
        self._mass = mass
        self._color = color
        self._image_file = image_file

        # Pymunk properties
        points = [(-width/2, -height/2), (width/2, -height/2),
                  (width/2, height/2), (-width/2, height/2)]
        inertia = pymunk.moment_for_box(mass, width, height)
        self._body = pymunk.Body(mass, inertia)
        self._shape = pymunk.Poly(self._body, points)
        self._body.position = pos
        self._shape.friction = self._friction
        self._shape.elasticity = self._elasticity
        self._shape.collision_type = self.collision_type

        # A hack to be able to access the object via it's shape
        self._shape.__setattr__('obj', self)

        # Pygame properties
        if image_file is not None:
            self._baseimage = view.load_and_scale(image_file, (width, height))
        else:
            self._baseimage = pygame.Surface((width, height), pygame.SRCALPHA)
            # Set the background color
            self._baseimage.fill((255, 255, 255))
            # Set the color that is ignored when blitting (like a green screen)
            self._baseimage.set_colorkey((255, 255, 255))
            # Draw the image we want to actually draw onto the surface
            baserect = pygame.Rect(0, 0, width, height)
            pygame.draw.rect(self._baseimage, self._color, baserect)

        self.image = self._baseimage
        self.rect = self.image.get_rect()

    @classmethod
    def from_yaml(cls, loader, node):
        '''
        A constructor that YAML uses to create instances of this class.
        '''

        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        width = values['width']
        height = values['height']
        mass = values['mass']
        pos = values['pos']
        color = values['color']
        image_file = values['image']

        # Return an instance of the object
        return cls(width=width, height=height, mass=mass,
                   pos=pos, color=color, image_file=image_file)

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''
        A method used by YAML to represent an instance of this class.
        '''

        # Construct a dict containing only the properties (wrong word...)
        # we want to use in the representation

        mapping = {'width': instance._width,
                   'height': instance._height,
                   'mass': instance._mass,
                   'pos': instance._body.position,
                   'color': instance._color,
                   'image': instance._image_file}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)


class Circle(MovingShape):
    '''
    A class for circles.
    '''

    yaml_tag = '!Circle'

    def __init__(self, radius=20, mass=1.0, position=(100, 100),
                 color=(0, 0, 0), image_file=None):
        '''
        Constructor for Circle.

        Input:
            * radius: Int
                - The radius of the circle.
                - Default: 20
            * mass: Float
                - The mass of the circle.
                - Default: 1.0
            * position: 2-tuple of ints
                - The initial position of the circle.
                - Default: (100, 100)
            * color: 3-tuple of ints 0-255
                - The color of the circle in rgb.
                  If "image_file" is specified, "color" is ignored.
                - Default: (0, 0, 0)
            * image_file: String
                - The name of the file containing the image to be used
                  on the circle.
                  If set to None, the colour specified in "color"
                  is used instead.
                - Default: None
        '''

        MovingShape.__init__(self)

        self._radius = radius
        self._mass = mass
        self._position = position
        self._color = color
        self._image_file = image_file

        # Pymunk properties
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self._body = pymunk.Body(mass, inertia)
        self._shape = pymunk.Circle(self._body, radius, (0, 0))
        self._body.position = position
        self._shape.friction = self._friction
        self._shape.elasticity = self._elasticity
        self._shape.collision_type = self.collision_type

        # A hack to be able to access the object via it's shape
        self._shape.__setattr__('obj', self)

        # Pygame properties
        if image_file is not None:
            self._baseimage = view.load_and_scale(image_file,
                                                  (2*radius, 2*radius))
        else:
            self._baseimage = pygame.Surface((2*radius, 2*radius),
                                             pygame.SRCALPHA)
            # Set the background color
            self._baseimage.fill((255, 255, 255))
            # Set the color that is ignored when blitting (like a green screen)
            self._baseimage.set_colorkey((255, 255, 255))
            # Draw the image we want to actually draw onto the surface
            baserect = pygame.Rect(0, 0, 2*radius, 2*radius)
            pygame.draw.ellipse(self._baseimage, self._color, baserect)

        self.image = self._baseimage
        self.rect = self.image.get_rect()

    @classmethod
    def from_yaml(cls, loader, node):
        '''A constructor that YAML uses to create instances of this class'''
        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        radius = values['radius']
        mass = values['mass']
        position = values['pos']
        color = values['color']
        image_file = values['image']

        # Return an instance of the object
        return cls(radius=radius, mass=mass, position=position,
                   color=color, image_file=image_file)

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''A method used by YAML to represent an instance of this class'''
        # Construct a dict containing only the properties (wrong word...)
        # we want to use in the representation

        mapping = {'radius': instance._radius,
                   'mass': instance._mass,
                   'pos': instance._body.position,
                   'color': instance._color,
                   'image': instance._image_file}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)


class Boundary(StaticShape):
    '''
    A class for the boundaries of the world.
    Represented as an invisible line.
    '''

    yaml_tag = '!Boundary'

    def __init__(self, points=[(0, 0), (1, 1)], width=5.0,
                 friction=1.0, elasticity=0.8):
        '''
        Constructor for Boundary.

        Input:
            * points: List of two 2-tuples of ints
                - The end-points of the line representing the boundary.
                - Default: [(0, 0), (1, 1)]
            * width: Float
                - The width of the boundary.
                  The width can in most cases be left as the default;
                  the only important thing is that is should be wide enough
                  that nothing passes through by accident, but thin
                  enough that strange effects like that it seems like
                  objects are "hovering" start occuring.
                - Default: 5.0
            * friction: Float 0.0 - inf
                - The friction coefficient of the boundary (the mu-factor).
                  Higher value -> more friction.
                - Default: 1.0
            * elasticity: Float 0.0 - 1.0
                - The elasticity of the boundary.
                  Higher value -> "bouncier" collisions.
                  0.0 -> completely plastic collision -> no bounce.
                  1.0 -> completely elastic collision -> perfect bounce.
                - Default: 0.5
        '''

        StaticShape.__init__(self, friction=friction, elasticity=elasticity)

        self._shape = pymunk.Segment(self._body, points[0], points[1], width)

        self._shape.collision_type = self.collision_type

        self._points = points
        self._width = width
        self._shape.friction = self._friction
        self._shape.elasticity = self._elasticity

    @classmethod
    def from_yaml(cls, loader, node):
        '''
        A constructor that YAML uses to create instances of this class.
        '''

        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        points = values['points']
        width = values['width']
        friction = values['friction']
        elasticity = values['elasticity']

        # Return an instance of the object
        return cls(points=points, width=width,
                   friction=friction, elasticity=elasticity)

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''
        A method used by YAML to represent an instance of this class.
        '''

        # Construct a dict containing only the properties (wrong word...)
        # we want to use in the representation

        mapping = {'points': instance._points,
                   'width': instance._width,
                   'friction': instance._friction,
                   'elasticity': instance._elasticity}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)
