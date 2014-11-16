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


# The magic!!
if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
