import os

import yaml
import pygame

import gameclass
import scene

# TODO: Add the option to use images as background of
# the screen, textboxes and buttons


def load_menu(file_name):
    '''Loads the menu defined in the YAML-file found at "file_path"
    and blits everything to "screen"'''

    # Get the full relative path of the YAML-file
    fullname = os.path.join('menu', 'menu_files', file_name)

    # Load the YAML-file
    with open(fullname, 'r') as stream:
        item_dict = yaml.load(stream)

    background_color = item_dict['background']

    # Create a screen and background
    info = pygame.display.Info()
    screen = pygame.display.get_surface()
    background = pygame.Surface([info.current_w, info.current_h])
    background.fill(background_color)

    # Clear the screen and make the cursor visible
    screen.blit(background, (0, 0))
    pygame.mouse.set_visible(True)

    # Create list for storing buttons
    buttons = []

    # Handle the objects from the YAML-file
    for key in item_dict:
        for item in item_dict[key]:
            if key == 'buttons':
                # All buttons are blitted to the screen and added to the list
                screen.blit(item.get_text_object(), item.get_rect())
                buttons.append(item)
            elif key == 'textboxes':
                # All textboxes are blitted to the screen
                screen.blit(item.get_text_object(), item.get_rect())
            elif key == 'background':
                # The background is already taken care of
                pass
            else:
                # Something unknown encountered, print an error and ignore it
                print ('Unknown object found when loading menu: ',
                       item, ', with key: ', key)

    pygame.display.flip()

    return buttons


def load_level(file_name):
    '''Loads the level from the YAML-file found at "file_path".
    Returns a game-object'''
    # TODO: Add actual level loading

    # Get the full relative path of the YAML-file
    # fullname = os.path.join('level', 'level_files', file_name)

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
