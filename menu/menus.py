from __future__ import division

import pygame

from gameclass import Game as Game
import load_yaml


def run_menu(file_path):

    # Load the menu
    buttons = load_yaml.load_menu(file_path)

    # Create clock item
    clock = pygame.time.Clock()
    FPS = 30

    # A reference to the button that has been pressed
    # (Needed since if a button has been pressed we want
    # to break the loop and then perform the buttons event)
    pressed_button = None

    run = True
    while run:

        run, mouse_pos, clicked = Game.take_menu_input()

        if clicked:
            # Check if a button has been pressed
            for button in buttons:
                if button.pressed(mouse_pos):
                    pressed_button = button
                    run = False
                    break
        else:
            # TODO: Check if a button is being hovered
            pass
            # for button in buttons:
            #     button.set_hovered(button.pressed(mouse_pos))

        # Keep the fps down
        clock.tick(FPS)

    # We have broken out of the loop, check if a button has
    # been pressed; if so, perform its action
    if pressed_button is not None:
        pressed_button.perform_action()