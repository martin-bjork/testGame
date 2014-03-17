from __future__ import division
import traceback
import sys

import pygame

import view
import gameclass
import players
import scene

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
    run, direction, jump, toggle_pause = game.take_input()

    # Move the player according to input
    player.move(direction, jump)

    # Update all sprites
    all_sprites.update()

    # Update the world's physics
    space.step(1/fps)

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
    run, direction, jump, toggle_pause = game.take_input()

    # Keep the desired fps
    clock.tick(fps)

    return run, toggle_pause


def main():
    game = gameclass.Game()
    clock = pygame.time.Clock()
    screen, background = view.init_window()

    game.set_clock(clock)
    game.set_screen(screen)
    game.set_background(background)
    game.set_fps(FPS)

    space = scene.init_scene(game)
    game.set_space(space)

    player = players.Player(game)
    game.set_player(player)

    # Initialize Sprite Groups
    # (will be more useful when we have more moving sprites)
    # TODO: Maybe move to other function?
    all_sprites = pygame.sprite.RenderUpdates()
    game.set_sprite_group(all_sprites)

    all_sprites.add(player)

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


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
