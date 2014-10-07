from __future__ import division

import pygame
import pygame.locals as loc
import pymunk

from sound import sound_effects
import view
import shapes
import collision_callbacks as col_call


class Player(shapes.MovingShape):

    collision_type = col_call.PLAYER_TYPE

    yaml_tag = '!Player'

    def __init__(self, mass=1, radius=20, position=(100, 50)):
        shapes.MovingShape.__init__(self)

        self._mass = mass
        self._radius = radius

        # Pymunk properties
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self._body = pymunk.Body(mass, inertia)
        self._shape = pymunk.Circle(self._body, radius, (0, 0))
        self._body.position = position
        self._shape.friction = self._friction
        self._shape.elasticity = self._elasticity

        self._shape.collision_type = Player.collision_type

        # A hack to be able to access the player object via it's shape
        self._shape.__setattr__('obj', self)

        # Pygame properties
        self._baseimage = pygame.transform.scale(view.load_image('smiley.png'),
                                                 (2*radius, 2*radius))
        self.image = self._baseimage
        self.rect = self.image.get_rect()

        # Game properties
        self._keys = {'left': loc.K_a,
                      'right': loc.K_d,
                      'jump': loc.K_SPACE}
        self._jumping = False

        self._move_impulse = 20     # TODO: Tweak these to get good values
        self._jump_impulse = 500

        self._jump_sound = sound_effects.load_sound('boing.wav')
        self._jump_sound.set_volume(0.5)
        self._bounce_sound = sound_effects.load_sound('bounce_3.wav')

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

        # Return an instance of the object
        return Player(mass=mass, radius=radius, position=position)

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''A method used by YAML to represent an instance of this class'''
        # Construct a dict containing only the properties (wrong word...)
        # we want to use in the representation

        mapping = {'radius': instance._radius,
                   'mass': instance._mass,
                   'pos': instance._body.position}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)

    def move(self, direction, jump):
        '''Moves the player in the direction specified by "direction".
        "direction" is an integer: -1 for moving left, 1 for moving right,
        0 for not moving at all'''
        self._body.apply_impulse((direction*self._move_impulse, 0))
        if jump:
            self.jump()

    def jump(self):
        '''Makes the player jump'''
        if not self._jumping:
            self._jump_sound.play()
            self._body.apply_impulse((0, self._jump_impulse))
            self._jumping = True

    def play_bounce(self, level):
        self._bounce_sound.set_volume(level)
        self._bounce_sound.play()

    # Getters/setters

    def get_keys(self):
        return self._keys

    def get_jumping(self):
        return self._jumping

    def set_jumping(self, jumping):
        self._jumping = jumping
