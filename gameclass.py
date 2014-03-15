# TODO: Change name? I don't like "gameclass"...

import pygame
import pygame.locals as loc


class Game:

    def __init__(self, player, clock):
        # TODO: Add more stuff
        self._player = player
        self._clock = clock

        self._keys_pressed = None
        self._keys_pressed_last_frame = None

    def take_input(self):
        '''Get input and handle it.'''

        run = True

        ### Get input
        self._keys_pressed = pygame.key.get_pressed()
        current_events = pygame.event.get()
        player_keys = self._player.get_keys()

        ### Handle non-keyboard events
        # Check if the window is closed, if so stop the game
        for event in current_events:
            if event.type == loc.QUIT:
                run = False

        ### Handle keyboard events
        # If the escape key is pressed, stop the game
        if self._keys_pressed[loc.K_ESCAPE]:
            run = False

        # Check in which direction the player should move.
        # 1 means right, -1 means left, 0 means stay put.
        direction = self._keys_pressed[player_keys['right']] -\
            self._keys_pressed[player_keys['left']]

        # Check if the player should jump
        # The "keys pressed last frame"-part is there to prevent
        # multiple jump-calls from when you just press the button once.
        jump = False
        if self._keys_pressed[player_keys['jump']] and \
                not self._keys_pressed_last_frame[player_keys['jump']]:
            jump = True

        self._keys_pressed_last_frame = self._keys_pressed

        return run, direction, jump

    # Getters/setters

    def get_player(self):
        return self._player

    def get_clock(self):
        return self._clock
