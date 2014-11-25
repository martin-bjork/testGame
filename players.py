from __future__ import division

import pygame.locals as loc

from sound import sound_effects
import shapes
import collision_callbacks as col_call


class Player(shapes.MovingShape):
    '''
    A class for handling the user controlled entity in the game.
    '''

    collision_type = col_call.PLAYER_TYPE

    yaml_tag = '!Player'

    def __init__(self, obj=shapes.Circle(),
                 move_impulse=20.0, jump_impulse=500.0,
                 jump_sound_file='boing.wav', bounce_sound_file='bounce_3.wav',
                 jump_sound_vol=0.5, bounce_sound_vol=0.5):
        '''
        Constructor for the Player class.

        Input:
            * obj: shapes.Shape
                - The Shape object that the user will control.
                - Default: shapes.Circle()
            * move_impulse: Float
                - The magnitude of the impulse impulse that should be applied
                  each time step to move the player.
                  Higher value -> faster movement.
                - Default: 20.0
            * jump_impulse: Float
                - The magnitude of the impulse impulse that should be applied
                  each time step to make the player jump.
                  Higher value -> higher jump.
                - Default: 500.0
            * jump_sound_file: String
                - The name of the file containing the sound that should be
                  played when the player jumps.
                - Default: 'boing.wav'
            * bounce_sound_file: String
                - The name of the file containing the sound that should be
                  played when the player collides with something.
                - Default: 'bounce_3.wav'
            * jump_sound_vol: Float
                - The volume of the jump sound, in the interval 0.0-1.0
                - Default: 0.5
            * bounce_sound_vol: Float
                - The volume of the collision sound, in the interval 0.0-1.0
                - Default: 0.5
        '''

        self._object = obj
        self._object.get_shape().collision_type = self.collision_type
        # A hack to be able to access the player via the shape
        self._object.get_shape().__setattr__('player', self)

        # Game properties
        # TODO: Set these via settings file
        self._keys = {'left': loc.K_a,
                      'right': loc.K_d,
                      'jump': loc.K_SPACE}
        self._jumping = False

        self._move_impulse = move_impulse
        self._jump_impulse = jump_impulse

        self._jump_sound_file = jump_sound_file
        self._bounce_sound_file = bounce_sound_file
        self._jump_sound_vol = jump_sound_vol
        self._bounce_sound_vol = bounce_sound_vol

        self._jump_sound = sound_effects.load_sound(jump_sound_file)
        self._jump_sound.set_volume(jump_sound_vol)
        self._bounce_sound = sound_effects.load_sound(bounce_sound_file)
        self._bounce_sound.set_volume(bounce_sound_vol)

    @classmethod
    def from_yaml(cls, loader, node):
        '''
        A constructor that YAML uses to create instances of this class.
        '''

        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        obj = values['obj']
        move_impulse = values['move_impulse']
        jump_impulse = values['jump_impulse']
        jump_sound_file = values['jump_sound_file']
        bounce_sound_file = values['bounce_sound_file']
        jump_sound_vol = values['jump_sound_vol']
        bounce_sound_vol = values['bounce_sound_vol']

        # Return an instance of the object
        return cls(obj=obj,
                   move_impulse=move_impulse, jump_impulse=jump_impulse,
                   jump_sound_file=jump_sound_file,
                   bounce_sound_file=bounce_sound_file,
                   jump_sound_vol=jump_sound_vol,
                   bounce_sound_vol=bounce_sound_vol)

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''
        A method used by YAML to represent an instance of this class.
        '''

        # Construct a dict containing only the properties
        # we want to use in the representation

        mapping = {'obj': instance._object,
                   'move_impulse': instance._move_impulse,
                   'jump_impulse': instance._jump_impulse,
                   'jump_sound_file': instance._jump_sound_vol,
                   'bounce_sound_file': instance._bounce_sound_file,
                   'jump_sound_vol': instance._jump_sound_vol,
                   'bounce_sound_vol': instance._bounce_sound_vol}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)

    def move(self, direction, jump):
        '''
        Moves the player in the direction specified by "direction".

        Input:
            * direction: Int
                - The direction in which the player should move.
                  1 -> right, -1 -> left, 0 -> no movement.
            * jump: Bool
                - Whether or not the player should jump.
        '''

        self._object._body.apply_impulse((direction*self._move_impulse, 0))
        if jump:
            self.jump()

    def jump(self):
        '''
        Makes the player jump if it is not already jumping.
        '''

        if not self._jumping:
            self._jump_sound.play()
            self._object._body.apply_impulse((0, self._jump_impulse))
            self._jumping = True

    def play_bounce(self, level):
        '''
        Plays the players bounce sound.

        Input:
            * level: Float
                - The volume that the sound should be played at.
        '''
        self._bounce_sound.set_volume(level)
        self._bounce_sound.play()

    # Getters/setters

    def get_object(self):
        return self._object

    def get_keys(self):
        return self._keys

    def get_jumping(self):
        return self._jumping

    def set_jumping(self, jumping):
        self._jumping = jumping

    def get_pos(self):
        return self._object.get_pos()
