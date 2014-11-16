import pygame

from gameclass import Game as Game
import load_yaml


def run_menu(file_path):

    # Load the menu
    buttons, obj_group, screen, background = load_yaml.load_menu(file_path)

    # Create clock item
    clock = pygame.time.Clock()
    FPS = 60

    run = True
    while run:

        run, pressed_button, open_pop_up = menu_loop(buttons, clock, FPS,
                                                     obj_group, screen)

        if open_pop_up:
            run_pop_up_menu('quit_game_pop_up.yaml')
            # Redraw screen to erase pop-up menu
            redraw(screen, background, obj_group)

    # We have broken out of the loop, check if a button has
    # been pressed; if so, perform its action
    if pressed_button is not None:
        pressed_button.perform_action()


def run_pop_up_menu(file_path):

    # Load the menu
    buttons, obj_group, background = load_yaml\
        .load_pop_up_menu(file_path)

    screen = pygame.display.get_surface()

    # Create clock item
    clock = pygame.time.Clock()
    FPS = 60

    run = True
    while run:

        run, pressed_button, open_pop_up = menu_loop(buttons, clock, FPS,
                                                     obj_group, screen)

    # We have broken out of the loop, check if a button has
    # been pressed; if so, perform its action
    if pressed_button is not None:
        pressed_button.perform_action()


def menu_loop(buttons, clock, FPS, obj_group, screen):

    mouse_pos, clicked, open_pop_up = Game.take_menu_input()

    run = True
    pressed_button = None

    if clicked:
        # Check if a button has been pressed
        for button in buttons:
            if button.pressed(mouse_pos):
                pressed_button = button
                run = False
                break
    else:
        for button in buttons:
            button.set_hovered(button.pressed(mouse_pos))

    # Keep the fps down
    clock.tick(FPS)

    # Redraw the screen
    dirty_rects = obj_group.draw(screen)
    pygame.display.update(dirty_rects)

    return run, pressed_button, open_pop_up


def redraw(screen, background, obj_group):
    screen.blit(background, (0, 0))

    for obj in obj_group:
        obj.dirty = 1

    pygame.display.flip()
