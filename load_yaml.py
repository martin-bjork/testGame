import yaml
import pygame

import menu_items


def load_menu(file_path, screen, background):
    '''Loads the menu defined in the YAML-file found at "file_path"
    and blits everything to "screen"'''

    # Clear the screen
    screen.blit(background, (0, 0))

    stream = file(file_path, 'r')
    item_dict = yaml.load(stream)

    for key in item_dict:
        item = item_dict[key]
        if isinstance(item, menu_items.MenuItem):
            screen.blit(item.get_text_object(), item.get_rect())
        else:
            print ('Unknown object found when loading menu: ',
                   item, ' with key ', key)

    pygame.display.flip()

    return item_dict
