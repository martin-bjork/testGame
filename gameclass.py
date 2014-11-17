# TODO: Change name? I don't like "gameclass"...
from __future__ import division

import pygame
import pygame.locals as loc


class Game:
    '''
    A class for storing information about the current game session.
    '''

    # These are set as class variables instead of instance variables
    # in order to be able to access them from static methods.
    _keys_pressed = None
    _keys_pressed_last_frame = None

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

    @classmethod
    def take_menu_input(cls):
        '''
        Retrieves input from the user and translates it into the information
        that is needed to run the menu.

        Output:
            * mouse_pos: 2-tuple of ints
                - The position of the mouse in screen coordinates.
            * clicked: Bool
                - Whether or not a mouse button has been clicked.
            * open_pop_up: Bool
                - Whether or not a pop-up menu should be opened.
        '''

        clicked = False
        open_pop_up = False

        # --- Get input ---

        cls._keys_pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        current_events = pygame.event.get()

        # --- Handle non-keyboard events ---

        for event in current_events:
            # Check if the user attempts to close the window,
            # if so open the pop-up menu
            if event.type == loc.QUIT:
                open_pop_up = True

            # Check if the mouse has been clicked
            elif event.type == loc.MOUSEBUTTONDOWN:
                clicked = True

        # --- Handle keyboard events ---

        # If the escape key is pressed, open pop-up menu
        if cls._keys_pressed[loc.K_ESCAPE] and \
                not cls._keys_pressed_last_frame[loc.K_ESCAPE]:
            open_pop_up = True

        # Save the keys that have been pressed this frame
        cls._keys_pressed_last_frame = cls._keys_pressed

        return mouse_pos, clicked, open_pop_up

    def take_game_input(self):
        '''
        Retrieves input from the user and translates it into the information
        that is needed to run the game.

        Output:
            * direction: Int
                - The direction in which the player should be moving.
                  1 -> right, -1 -> left, 0 -> no movement.
            * jump: Bool
                - Whether or not the player should jump.
            * open_pop_up: Bool
                - Whether or not a pop-up menu should be opened.
        '''

        open_pop_up = False

        # --- Get input ---

        self.__class__._keys_pressed = pygame.key.get_pressed()
        current_events = pygame.event.get()
        player_keys = self._player.get_keys()

        # --- Handle non-keyboard events ---

        # Check if the user attempts to close the window,
        # if so open the pop-up menu
        for event in current_events:
            if event.type == loc.QUIT:
                open_pop_up = True

        # --- Handle keyboard events ---

        # If the escape key is pressed, open pop-up menu
        if self.__class__._keys_pressed[loc.K_ESCAPE] and \
                not self.__class__._keys_pressed_last_frame[loc.K_ESCAPE]:
            open_pop_up = True

        # Check in which direction the player should move.
        # 1 means right, -1 means left, 0 means stay put.
        direction = self.__class__._keys_pressed[player_keys['right']] -\
            self.__class__._keys_pressed[player_keys['left']]

        # Check if the player should jump
        # The "keys pressed last frame"-part is there to prevent
        # multiple jump-calls from when you just press the button once.
        if self.__class__._keys_pressed[player_keys['jump']] and not \
                self.__class__._keys_pressed_last_frame[player_keys['jump']]:
            jump = True
        else:
            jump = False

        # Save the keys that have been pressed this frame
        self.__class__._keys_pressed_last_frame = self.__class__._keys_pressed

        return direction, jump, open_pop_up

    def game_loop(self):
        '''
        The game loop - handles everything that should happen
        in every frame of the game.

        Output:
            * open_pop_up: Bool
                - Whether or not a pop-up menu should be opened.
        '''

        # TODO: Add more game logic
        # NOTE: The game logic that is to be added perhaps belongs
        #       in the collision callbacks and the update-calls instead?

        # Take input
        direction, jump, open_pop_up = self.take_game_input()

        # Move the player according to input
        self._player.move(direction, jump)

        # Update all sprites
        self._sprite_group.update(self)

        # Update the world's physics
        self._space.step(1 / self._fps)

        # Draw all sprites that have moved
        dirty_sprites = self._sprite_group.draw(self._screen)
        pygame.display.update(dirty_sprites)

        # Keep the desired fps
        self._clock.tick(self._fps)

        return open_pop_up

    def redraw(self):
        '''
        Clears the screen, redraws the background and sets all sprites to dirty
        '''

        self._screen.blit(self._background, (0, 0))

        for sprite in self._sprite_group:
            sprite.dirty = 1

        pygame.display.flip()

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
        self._moving_objects.extend(objects)

    def get_moving_objects(self):
        return self._moving_objects

    def add_static_objects(self, *objects):
        self._static_objects.extend(objects)

    def get_static_objects(self):
        return self._static_objects
