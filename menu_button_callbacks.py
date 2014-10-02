import main
import menu


def play_level_goto_menu(level_file_path, menu_file_path):
    '''Loads the level specified in the YAML-file at "level_file_path",
    and when the level is finished loads the menu specified in the
    YAML-file at "menu_file_path".'''

    # Start the game
    main.run_level(level_file_path)

    # When the game has ended, return to main menu
    menu.run_menu(menu_file_path)


def goto_menu(menu_file_path):
    '''Loads the menu specified in the YAML-file at "menu_file_path".'''
    menu.run_menu(menu_file_path)
