import pygame
import pygame.locals as loc


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._keys = {'left': loc.K_a,
                      'right': loc.K_d,
                      'jump': loc.K_SPACE}

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
