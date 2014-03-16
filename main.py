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
    screen = view.init_window()

    game.set_clock(clock)
    game.set_screen(screen)

    space = scene.init_scene(game)
    game.set_space(space)

    player = players.Player(game)
    game.set_player(player)

    run = True

    # TODO: Add game logic here
    while run:
        # Take input
        run, direction, jump = game.take_input()

        # Move the player
        player.move(direction, jump)

        # TODO Add physics here
        # TODO: Add drawing of the screen here

        # TODO: Use update instead? It's probably faster
        pygame.display.flip()
        
        # Keep the desired fps
        clock.tick(FPS)

if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
