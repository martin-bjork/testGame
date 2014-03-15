# TODO: Change name? I don't like "gameclass"...

import pygame
import pygame.locals as loc


class Game:

    def __init__(self):
        # TODO: Add more stuff
        self._keys_pressed = None

    def take_input(self):
        '''Get input and handle it.'''

        run = True

        # Get input
        self._keys_pressed = pygame.key.get_pressed()
        current_events = pygame.event.get()

        # Handle non-keyboard events
        for event in current_events:
            if event.type == loc.QUIT:
                run = False

        # Handle keyboard events
        if self._keys_pressed[loc.K_ESCAPE]:
            run = False

        return run
