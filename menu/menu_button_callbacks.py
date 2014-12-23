# Callback functions for buttons in menus.
# They determine what happens when a button is pressed.

import sys

from menu import menus
from level import levels

# TODO: Decide if we should use better return values (e.g. a dict?)


def play_level(level_file_name):
    '''
    Runs the level specified in the YAML-file named "level_file_name".
    '''

    levels.run_level(level_file_name)


def goto_menu(menu_file_name):
    '''
    Loads the menu specified in the YAML-file named "menu_file_name".
    '''

    menus.run_menu(menu_file_name)


def open_popup_menu(popup_file_name):
    '''
    Loads the pop-up menu specified in the YAML-file named "popup_file_name".
    When the pop-up menu is closed, load the menu specified in
    the YAML-file named "menu_file_name".
    '''

    # Open pop-up menu
    menus.run_pop_up_menu(popup_file_name)
    return ReturnVal({'redraw': True})


def do_nothing():
    '''
    As the name implies - does nothing at all.
    '''

    pass


def exit_menu():
    '''
    Exits the current menu
    '''

    return ReturnVal({'exit': True, 'redraw': True})


def quit_game():
    '''
    Quits the game.
    '''

    sys.exit()


class ReturnVal():
    '''
    A class for storing the return values of the button callbacks.
    Behaves kind of as a simple dict, but returns None if the key
    doesn't exist instead of throwing an exception.
    '''

    # TODO: Inherit from dict instead?

    def __init__(self, dictionary):
        self._dict = dictionary

    def __getitem__(self, key):
        try:
            return self._dict[key]
        except KeyError:
            return None
