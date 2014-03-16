import pygame
import pygame.locals as loc
import pymunk

import scene


class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self._keys = {'left': loc.K_a,
                      'right': loc.K_d,
                      'jump': loc.K_SPACE}

        # Currently a circle, create a more interesting shape later
        radius = 20
        mass = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self._body = pymunk.Body(mass, inertia)
        self._shape = pymunk.Circle(self._body, radius, (0, 0))

        space = game.get_space()
        space.add(self._body, self._shape)

        width, height = game.get_screen_size()
        self._image = pygame.Surface((2*radius, 2*radius))
        pygame.draw.circle(self._image, (255, 0, 0),
                           scene.pymunk_to_pygame_coords(
                               self._body.position.x,
                               self._body.position.y, height),
                           radius, 2)

        # TODO: Add more, such as image etc

    def move(self, direction, jump):
        '''Moves the player in the direction specified by "direction".
        "direction" is an integer: -1 for moving left, 1 for moving rigth,
        0 for not moving at all'''
        # TODO: Add this
        if direction != 0:
            print 'Moved; direction: {dir}'.format(dir=direction)
        if jump:
            self._jump()
        pass

    def _jump(self):
        '''Makes the player jump'''
        # TODO: Add this
        print 'Jumped'
        pass

    # Getters/setters

    def get_keys(self):
        return self._keys

    def get_body(self):
        return self._body

    def get_shape(self):
        return self._shape

    def get_image(self):
        return self._image
