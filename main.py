from __future__ import division
import traceback
import sys

import pygame

import view
import gameclass
import scene
import load_yaml

FPS = 60
# NOTE: Made game global for convenience, maybe consider other solutions?
global game


def main():
    '''The main function for the game - everything starts here'''

    # Create a game object and initialize the window
    # FIXME: For some reason, the game object doesn't seem to have been
    # initialized when game_main() is called. Might be since it is called
    # from another module?
    global game
    game = gameclass.Game()
    screen, background = view.init_window()

    game.set_screen(screen)
    game.set_background(background)
    clock = pygame.time.Clock()
    game.set_clock(clock)
    game.set_fps(FPS)

    # Load the menu
    items = load_yaml.load_menu('menu.yaml')

    # Assign names to the buttons in the menu
    play_button = items['play_button']
    quit_button = items['quit_button']

    # NOTE: Have to manually add this here, don't know any other way...
    # play_button.set_action_args([game])

    pygame.display.flip()

    run = True
    while run:

        run, mouse_pos = game.take_menu_input()

        if mouse_pos:
            if play_button.pressed(mouse_pos):
                # Start the game
                play_button.perform_action()

            elif quit_button.pressed(mouse_pos):
                run = False

        # Keep the fps down
        clock.tick(30)


def game_main():
    '''The main function of the game - loads a level and runs it'''

    global game

    # Set up the background
    screen = game.get_screen()
    background = game.get_background()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.mouse.set_visible(False)

    # Set up the physics and player
    scene.init_scene(game)

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


# TODO: Move this function
def play_button_callback():
    '''Function to be called when the play button is pressed'''

    # Start the game
    game_main()

    items = load_yaml.load_menu('menu.yaml')
    pygame.mouse.set_visible(True)


# The magic!!
if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
