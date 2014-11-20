# Callback functions for buttons in menus.
# They determine what happens when a button is pressed.

import sys

from menu import menus
from level import levels


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


def open_popup_menu(popup_file_name, menu_file_name):
    '''
    Loads the pop-up menu specified in the YAML-file named "popup_file_name".
    When the pop-up mneu is closed, load the menu specified in
    the YAML-file named "menu_file_name".
    '''

    # Open pop-up menu
    menus.run_pop_up_menu(popup_file_name)
    # Open the other menu if the pop-up menu is closed
    goto_menu(menu_file_name)


def do_nothing():
    '''
    As the name implies - does nothing at all.
    '''

    pass


def quit_game():
    '''
    Quits the game.
    '''

    sys.exit()
