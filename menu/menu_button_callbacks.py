import sys

import main
from menu import menus


def play_level_goto_menu(level_file_path, menu_file_path):
    '''Loads the level specified in the YAML-file at "level_file_path",
    and when the level is finished loads the menu specified in the
    YAML-file at "menu_file_path".'''

    # Start the game
    main.run_level(level_file_path)

    # When the game has ended, return to main menu
    menus.run_menu(menu_file_path)


def play_level(level_file_path):
    main.run_level(level_file_path)


def goto_menu(menu_file_path):
    '''Loads the menu specified in the YAML-file at "menu_file_path".'''
    menus.run_menu(menu_file_path)


def do_nothing():
    pass


def quit_game():
    sys.exit()
