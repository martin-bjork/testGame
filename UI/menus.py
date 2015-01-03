# Functions for running menus.

import pygame

from GamePlay.gameclass import Game as Game
from Tools import load_yaml


def run_menu(file_name):
    '''
    Runs the menu specified in the YAML-file called "file_name".

    Input:
        * file_name: String
            - The name of the YAML-file describing the menu.
    '''

    # Load the menu
    buttons, obj_group, screen, background = load_yaml.load_menu(file_name)

    # Create clock item
    clock = pygame.time.Clock()
    FPS = 60

    while True:

        pressed_button, open_pop_up = menu_loop(buttons, clock, FPS,
                                                obj_group, screen)

        if pressed_button is not None:
            return_val = pressed_button.perform_action()
            if return_val['exit']:
                return
            elif return_val['redraw']:
                redraw(screen, background, obj_group)

        if open_pop_up:
            run_pop_up_menu('quit_game_pop_up.yaml')
            # Clear the screen when closing the menu
            redraw(screen, background, obj_group)


def run_pop_up_menu(file_name):
    '''
    Runs the pop-up menu specified in the YAML-file called "file_name".

    Input:
        * file_name: String
            - The name of the YAML-file describing the pop-up menu.
    '''

    # Load the menu
    buttons, obj_group, background = load_yaml\
        .load_pop_up_menu(file_name)

    screen = pygame.display.get_surface()

    # Create clock item
    clock = pygame.time.Clock()
    FPS = 60

    while True:

        pressed_button, open_pop_up = menu_loop(buttons, clock, FPS,
                                                obj_group, screen)

        if pressed_button is not None:
            return_val = pressed_button.perform_action()
            if return_val['exit']:
                return


def menu_loop(buttons, clock, FPS, obj_group, screen):
    '''
    The code that should be run each iteration when running the menu.
    Takes input, checks if buttons have been pressed and redraws the screen.
    '''

    mouse_pos, clicked, open_pop_up = Game.take_menu_input()

    pressed_button = None

    if clicked:
        # Check if a button has been pressed
        for button in buttons:
            if button.pressed(mouse_pos):
                pressed_button = button
                break
    else:
        for button in buttons:
            button.set_hovered(button.pressed(mouse_pos))

    # Keep the fps down
    clock.tick(FPS)

    # Redraw the screen
    dirty_rects = obj_group.draw(screen)
    pygame.display.update(dirty_rects)

    return pressed_button, open_pop_up


def redraw(screen, background, obj_group):
    '''
    Redraws the everything on screen.

    Input:
        * screen: pygame.Surface
            - The screen of the current window, onto which
              everything is to be drawn.
        * background: pygame.Surface
            - The background image that is to be drawn on the screen.
        * obj_group: pygame.sprite.SpriteGroup
            - A container with all objects that are to be drawn on the screen.
    '''

    # TODO: Move this?

    # Clear the screen
    screen.blit(background, (0, 0))

    # Set all objects to dirty so they are redrawn.
    for obj in obj_group:
        obj.dirty = 1

    # Update the window
    pygame.display.flip()
