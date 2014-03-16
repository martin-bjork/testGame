import traceback
import sys

import pygame

import view
import gameclass
import players

FPS = 60


def main():
    clock = pygame.time.Clock()
    screen = view.set_up_window()
    player = players.Player()
    game = gameclass.Game(player, clock, screen)

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
