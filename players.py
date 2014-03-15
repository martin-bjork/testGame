import pygame
import pygame.locals as loc


class Player:

    def __init__(self):
        self._pos = [0, 0]
        self._keys = {'left': loc.K_a,
                      'right': loc.K_d,
                      'jump': loc.K_SPACE}

        # TODO: Add more, such as image etc

    def move(self, direction):
        '''Moves the player in the direction specified by "direction".
        "direction" is an integer: -1 for moving left, 1 for moving rigth,
        0 for not moving at all'''
        # TODO: Add this
        if direction != 0:
            print 'Moved; direction: {dir}'.format(dir=direction)
        pass

    def jump(self):
        '''Makes the player jump'''
        # TODO: Add this
        print 'Jumped'
        pass

    # Getters/setters

    def get_pos(self):
        return self._pos

    def get_keys(self):
        return self._keys
