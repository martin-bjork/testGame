from __future__ import division

import pygame
import pygame.locals as loc
import pymunk

from sound import sound_effects
import view
import shapes


class Player(shapes.MovingShape):

    collision_type = 3

    def __init__(self, space, mass=1, radius=20, position=(100, 50)):
        super(Player, self).__init__()

        # Pymunk properties
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self._body = pymunk.Body(mass, inertia)
        self._shape = pymunk.Circle(self._body, radius, (0, 0))
        self._body.position = position

        space.add(self._body, self._shape)
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

    def move(self, direction, jump):
        '''Moves the player in the direction specified by "direction".
        "direction" is an integer: -1 for moving left, 1 for moving rigth,
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
