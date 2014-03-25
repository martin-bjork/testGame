from __future__ import division
from math import pi

import pygame
import pygame.locals as loc
import pymunk

from sound import sound_effects
import scene
import view


class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        # TODO: Clean up this mess...
        pygame.sprite.Sprite.__init__(self)
        self._keys = {'left': loc.K_a,
                      'right': loc.K_d,
                      'jump': loc.K_SPACE}

        width, height = game.get_screen_size()

        # NOTE: Currently a smiley, create a more interesting shape later
        radius = 20
        mass = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self._body = pymunk.Body(mass, inertia)
        self._shape = pymunk.Circle(self._body, radius, (0, 0))
        self._body.position = width/2, radius + 10
        self._shape.friction = 1.0
        self._shape.elasticity = 0.5

        # A hack to be able to access the player object via it's shape
        self._shape.__setattr__('obj', self)

        space = game.get_space()
        space.add(self._body, self._shape)

        self._baseimage = pygame.transform.scale(view.load_image('smiley.png'),
                                                 (2*radius, 2*radius))
        self.image = self._baseimage
        self.rect = self.image.get_rect()

        self._jumping = False

        # TODO: Tweak these to get good values
        self._move_impulse = 20
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
            self._jump()

    def _jump(self):
        '''Makes the player jump'''
        if not self._jumping:
            self._jump_sound.play()
            self._body.apply_impulse((0, self._jump_impulse))
            self._jumping = True

    def update(self):
        '''Updates the position of the sprite to match
        the position of it's body.'''
        self.image = pygame.transform.rotate(self._baseimage,
                                             self._body.angle*180/pi)
        self.rect = self.image.get_rect()
        self.rect.center = scene.pymunk_to_pygame_coords(self._body.position[0],
                                                         self._body.position[1],
                                                         480)

    def play_bounce(self, level):
        self._bounce_sound.set_volume(level)
        self._bounce_sound.play()

    # Getters/setters

    def get_keys(self):
        return self._keys

    def get_body(self):
        return self._body

    def get_shape(self):
        return self._shape

    def get_image(self):
        return self.image

    def get_acceleration(self):
        return self._acceleration

    def get_jumping(self):
        return self._jumping

    def set_jumping(self, jumping):
        self._jumping = jumping
