import yaml
import pygame

import menu_items
import text_boxes
import gameclass
import scene


def load_menu(file_path):
    '''Loads the menu defined in the YAML-file found at "file_path"
    and blits everything to "screen"'''

    # Create a screen and background
    info = pygame.display.Info()
    screen = pygame.display.get_surface()
    background = pygame.Surface([info.current_w, info.current_h])
    background.fill((200, 200, 200))    # TODO: Get color from the YAML-file?

    # Clear the screen
    screen.blit(background, (0, 0))

    with open(file_path, 'r') as stream:
        item_dict = yaml.load(stream)

    for key in item_dict:
        item = item_dict[key]
        if isinstance(item, menu_items.MenuItem) or \
                isinstance(item, text_boxes.TextBox):
            screen.blit(item.get_text_object(), item.get_rect())
        else:
            print ('Unknown object found when loading menu: ',
                   item, ' with key ', key)

    pygame.display.flip()

    return item_dict


def load_level(file_path):
    '''Loads the level from the YAML-file found at "file_path".
    Returns a game-object'''
    # TODO: Add actual level loading

    # Create game object
    game = gameclass.Game()

    # Create a screen and background
    info = pygame.display.Info()
    screen = pygame.display.get_surface()
    background = pygame.Surface([info.current_w, info.current_h])
    background.fill((200, 200, 200))    # TODO: Get color from the YAML-file?

    # Create other game related objects
    FPS = 60
    clock = pygame.time.Clock()

    # Add the objects to the game-object
    game.set_screen(screen)
    game.set_background(background)
    game.set_clock(clock)
    game.set_fps(FPS)

    # TODO: Everything that is created in this function call should
    # really be loaded from the YAML-file. In fact, I think that
    # the entire module "scene" can be removed in favour of this module.
    scene.init_scene(game)

    # Clear the screen and hide the cursor
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.mouse.set_visible(False)

    return game
