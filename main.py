import traceback
import sys

import pygame

import view
import gameclass

FPS = 60


def main():
    game = gameclass.Game()
    clock = pygame.time.Clock()
    view.set_up_window()

    run = True

    # TODO: Add game logic here
    while run:
        run = game.take_input()
        clock.tick(FPS)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
