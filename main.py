from __future__ import division
import traceback
import sys

import pygame

import view
import gameclass
import players
import scene

FPS = 60


def main():
    game = gameclass.Game()
    clock = pygame.time.Clock()
    screen, background = view.init_window()

    game.set_clock(clock)
    game.set_screen(screen)
    game.set_background(background)

    space = scene.init_scene(game)
    game.set_space(space)

    player = players.Player(game)
    game.set_player(player)

    # Initialize Sprite Groups 
    # (will be more useful when we have more moving sprites)
    # TODO: Maybe move to other function?
    all_sprites = pygame.sprite.RenderUpdates()

    all_sprites.add(player)

    # TODO: Add more game logic here
    run = True
    while run:

        # Clear the sprites
        all_sprites.clear(screen, background)

        # Take input
        run, direction, jump = game.take_input()

        # Move the player according to input
        player.move(direction, jump)

        # Update all sprites
        all_sprites.update()

        # Update the world's physics
        space.step(1/FPS)

        dirty_sprites = all_sprites.draw(screen)
        pygame.display.update(dirty_sprites)

        # Keep the desired fps
        clock.tick(FPS)

if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
