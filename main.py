from __future__ import division
import traceback
import sys

import pygame

import view
import load_yaml
import menu


def main():
    '''The main function for the game - everything starts here'''

    # Initialize a window
    screen, background = view.init_window()

    # Load the main menu
    menu.run_menu('main_menu.yaml')


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
            run, toggle_pause = game_loop(game)
        else:
            run, toggle_pause = pause_loop(game)

    # Fade out the music after quitting the game
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(500)
        pygame.time.wait(500)


def game_loop(game):
    '''The game loop - handles everything that should happen
    in every frame of the game'''

    # TODO: Add more game logic

    screen = game.get_screen()
    background = game.get_background()
    all_sprites = game.get_sprite_group()
    player = game.get_player()
    space = game.get_space()
    fps = game.get_fps()
    clock = game.get_clock()

    # Clear the sprites
    # NOTE: Is this necessary? This makes the whole business with
    # dirty sprites unnecessary?
    all_sprites.clear(screen, background)

    # Take input
    run, direction, jump, toggle_pause = game.take_game_input()

    # Move the player according to input
    player.move(direction, jump)

    # Update all sprites
    all_sprites.update(game)

    # Update the world's physics
    space.step(1 / fps)

    # Draw all sprites that have moved
    dirty_sprites = all_sprites.draw(screen)
    pygame.display.update(dirty_sprites)

    # Keep the desired fps
    clock.tick(fps)

    return run, toggle_pause


def pause_loop(game):
    '''Everything that happens when the game is paused - it just waits
        for input telling it not to pause any more'''

    clock = game.get_clock()
    fps = game.get_fps()

    # Take input
    run, direction, jump, toggle_pause = game.take_game_input()

    # Keep the desired fps
    clock.tick(fps)

    return run, toggle_pause


# The magic!!
if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
