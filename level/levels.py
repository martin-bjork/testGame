# Functions for running levels.

import pygame

import load_yaml
from menu import menus


def run_level(file_path):
    '''
    The main function of the game - loads a level and runs it.

    Input:
        * file_path: String
            - The name of the YAML-file describing the level.
    '''

    # Load the level
    game = load_yaml.load_level(file_path)

    while True:

        # Run one iteration of the game.
        open_pop_up = game.game_loop()

        # Open a pop-up menu if told to do so.
        if open_pop_up:
            # The loop can be terminated from within run_pop_up_menu()
            # by e.g. loading another level/menu/closing the application.
            menus.run_pop_up_menu('quit_level_pop_up.yaml')
            # Force all items to be redrawn to erase the pop-up menu
            # and set the mouse to invisible
            game.redraw()
            pygame.mouse.set_visible(False)
