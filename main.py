from __future__ import division
import traceback
import sys

import pygame

import view
import load_yaml
from menu import menus


def main():
    '''The main function for the game - everything starts here'''

    # Initialize a window
    screen, background = view.init_window()

    # Load the main menu
    menus.run_menu('main_menu.yaml')


def run_level(file_path):
    '''The main function of the game - loads a level and runs it'''

    # Load the level
    game = load_yaml.load_level(file_path)

    while True:

        open_pop_up = game.game_loop()

        if open_pop_up:
            # The loop can be terminated from within run_pop_up_menu()
            # by e.g. loading another level/menu/closing the application.
            menus.run_pop_up_menu(game.get_screen(), 'quit_level_pop_up.yaml')
            # Force all items to be redrawn to erase the pop-up menu
            game.redraw()


# The magic!!
if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
