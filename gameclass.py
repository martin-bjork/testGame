# TODO: Change name? I don't like "gameclass"...

import pygame
import pygame.locals as loc


class Game:

    def __init__(self):
        # TODO: Add more stuff
        self._player = None
        self._moving_objects = []
        self._static_objects = []
        self._clock = None
        self._screen = None
        self._screenrect = None
        self._space = None
        self._background = None
        self._fps = None
        # TODO: Add option for more sprite groups when needed
        self._sprite_group = None

        self._keys_pressed = None
        self._keys_pressed_last_frame = None

    @staticmethod
    def take_menu_input():
        '''Get input for the menu'''

        run = True
        clicked = False
        mouse_pos = pygame.mouse.get_pos()

        current_events = pygame.event.get()

        for event in current_events:
            if event.type == loc.QUIT:
                run = False
            elif event.type == loc.KEYDOWN and event.key == loc.K_ESCAPE:
                run = False
            elif event.type == loc.MOUSEBUTTONDOWN:
                clicked = True

        return run, mouse_pos, clicked

    def take_game_input(self):
        '''Get input for the game loop and handle it.'''

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
        # NOTE: The "keys pressed last frame"-part is there to prevent
        # multiple jump-calls from when you just press the button once.
        if self._keys_pressed[player_keys['jump']] and \
                not self._keys_pressed_last_frame[player_keys['jump']]:
            jump = True
        else:
            jump = False

        # Check if the game should be paused
        if self._keys_pressed[loc.K_p] and \
                not self._keys_pressed_last_frame[loc.K_p]:
            toggle_pause = True
        else:
            toggle_pause = False

        self._keys_pressed_last_frame = self._keys_pressed

        return run, direction, jump, toggle_pause

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

    def get_fps(self):
        return self._fps

    def set_fps(self, fps):
        self._fps = fps

    def get_sprite_group(self):
        return self._sprite_group

    def set_sprite_group(self, sprite_group):
        self._sprite_group = sprite_group

    def add_moving_objects(self, *objects):
        for obj in objects:
            self._moving_objects.append(obj)

    def get_moving_objects(self):
        return self._moving_objects

    def add_static_objects(self, *objects):
        for obj in objects:
            self._static_objects.append(obj)

    def get_static_objects(self):
        return self._static_objects
