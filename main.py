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

    run = True
    pause = False
    toggle_pause = False

    while run:

        if toggle_pause:
            pause = not pause
            # Show the mouse if paused, hide if running
            pygame.mouse.set_visible(int(pause))

        if not pause:
            run, toggle_pause = game.game_loop()
        else:
            run, toggle_pause = game.pause_loop()

    # Fade out the music after quitting the game
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(500)
        pygame.time.wait(500)


# The magic!!
if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
