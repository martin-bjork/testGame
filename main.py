# The main file, from which the game is started.

from __future__ import division
import traceback
import sys

import pygame

import view
from menu import menus


def main():
    '''
    The main function of the game - everything starts here!
    Initializes a window and loads the main menu.
    '''

    # Initialize a window
    view.init_window()

    # Load the main menu
    menus.run_menu('main_menu.yaml')


# Run the game and handle exceptions
if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
