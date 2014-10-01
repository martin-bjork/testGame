import yaml
import pygame

import menu_items
import text_boxes


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
