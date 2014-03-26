from __future__ import division
import traceback
import sys

import pygame

import view
import gameclass
import scene
import buttons

FPS = 60


def game_loop(game):
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

    clock = game.get_clock()
    fps = game.get_fps()

    # Take input
    run, direction, jump, toggle_pause = game.take_game_input()

    # Keep the desired fps
    clock.tick(fps)

    return run, toggle_pause


def game_main(game):

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


def main():

    # Create a game object and initialize the window
    game = gameclass.Game()
    screen, background = view.init_window()

    game.set_screen(screen)
    game.set_background(background)
    clock = pygame.time.Clock()
    game.set_clock(clock)
    game.set_fps(FPS)

    # Create some buttons
    play_button = buttons.Button('Play', 300, 200)
    quit_button = buttons.Button('Quit', 300, 280)
    screen.blit(play_button.get_text_object(), play_button.get_rect())
    screen.blit(quit_button.get_text_object(), quit_button.get_rect())

    pygame.display.flip()

    run = True
    while run:

        run, mouse_pos = game.take_menu_input()

        if mouse_pos:
            if play_button.pressed(mouse_pos):
                # Start the game
                game_main(game)

                # Reset the screen after the game has ended
                screen.blit(background, (0, 0))
                screen.blit(play_button.get_text_object(),
                            play_button.get_rect())
                screen.blit(quit_button.get_text_object(),
                            quit_button.get_rect())
                pygame.mouse.set_visible(True)

                pygame.display.flip()

            elif quit_button.pressed(mouse_pos):
                run = False

        # Keep the fps down
        clock.tick(30)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
