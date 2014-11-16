import sys

from menu import menus
from level import levels


def play_level(level_file_path):
    levels.run_level(level_file_path)


def goto_menu(menu_file_path):
    '''Loads the menu specified in the YAML-file at "menu_file_path".'''
    menus.run_menu(menu_file_path)


def open_popup_menu(popup_file_path, menu_file_path):
    # Open pop-up menu
    menus.run_pop_up_menu(popup_file_path)
    # Open the other menu if the pop-up menu is closed
    menus.run_menu(menu_file_path)


def do_nothing():
    pass


def quit_game():
    sys.exit()
