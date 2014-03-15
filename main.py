from __future__ import division
import traceback
import sys

import pygame


def main():
    pygame.init()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
