# TODO: Change name? I don't like "gameclass"...

import pygame
import pygame.locals as loc


class Game:

    def __init__(self):
        # TODO: Add more stuff
        self._player = None
        self._clock = None
        self._screen = None
        self._screenrect = None
        self._space = None
        self._background = None

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

    def set_player(self, player):
        self._player = player

    def get_clock(self):
        return self._clock

    def set_clock(self, clock):
        self._clock = clock

    def get_screen(self):
        return self._screen

    def set_screen(self, screen):
        self._screen = screen
        self._screenrect = screen.get_rect()

    def get_screenrect(self):
        return self._screenrect

    def get_screen_size(self):
        return self._screen.get_size()

    def get_space(self):
        return self._space

    def set_space(self, space):
        self._space = space

    def get_background(self):
        return self._background

    def set_background(self, background):
        self._background = background
