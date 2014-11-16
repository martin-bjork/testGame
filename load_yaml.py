import os

import yaml
import pygame
import pymunk

import gameclass
import collision_callbacks as col_call
import view

# YAML needs these imports to be able to create the objects
from menu import menu_items
import shapes
import players

# TODO: Add a "To YAML"-function?
# TODO: Better docstrings


def load_menu(file_name):
    '''
    Loads the menu defined in the YAML-file named "file_name"
    '''

    # Get the full relative path of the YAML-file
    fullname = os.path.join('menu', 'menu_files', file_name)

    # Load the YAML-file
    with open(fullname, 'r') as stream:
        item_dict = yaml.load(stream)

    # Create a screen and background
    background_image_file = item_dict['background_file']
    background_color = item_dict['background']
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    screen = pygame.display.get_surface()

    if background_image_file is not None:
        background = pygame.transform\
            .smoothscale(view.load_image(background_image_file),
                         (width, height))
    else:
        background = pygame.Surface([width, height])
        background.fill(background_color)

    # Clear the screen and make the cursor visible
    screen.blit(background, (0, 0))
    pygame.mouse.set_visible(True)

    # Create lists for storing buttons and all objects that should be drawn
    buttons = []
    objs = []

    # Handle the objects from the YAML-file
    for key in item_dict:
        if key == 'background':
            pass
        elif key == 'background_file':
            pass
        else:
            for item in item_dict[key]:
                if key == 'buttons':
                    buttons.append(item)
                    objs.append(item)
                elif key == 'textboxes':
                    objs.append(item)
                elif key == 'music':
                    music_file = item['file']
                    vol = item['vol']
                else:
                    # Something unknown encountered, print an error and ignore
                    print ('Unknown object found when loading menu: ',
                           item, ', with key: ', key)

    # Create a Sprite group for the objects
    obj_group = pygame.sprite.LayeredDirty(*objs)
    # Set the background of the Sprite group
    obj_group.clear(screen, background)

    pygame.display.flip()

    # Start the music
    # TODO: Find a way to not restart the music if the currently
    # playing file is to be loaded.
    # TODO: Add smooth fading between songs.
    if music_file is not None:
        full_music_file = os.path.join('sound', 'sound_data', music_file)
        pygame.mixer.music.load(full_music_file)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(-1)

    return buttons, obj_group, screen, background


def load_level(file_name):
    '''
    Loads the level from the YAML-file named "file_name".
    Returns a game-object.
    '''

    # Get the full relative path of the YAML-file
    fullname = os.path.join('level', 'level_files', file_name)

    # Load the YAML-file
    with open(fullname, 'r') as stream:
        item_dict = yaml.load(stream)

    # Create game object
    game = gameclass.Game()

    # Create a screen and background
    background_image_file = item_dict['background_file']
    background_color = item_dict['background']
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    screen = pygame.display.get_surface()

    if background_image_file is not None:
        background = pygame.transform\
            .smoothscale(view.load_image(background_image_file),
                         (width, height))
    else:
        background = pygame.Surface([width, height])
        background.fill(background_color)

    # Create other game related objects
    FPS = 60
    clock = pygame.time.Clock()

    # Add the objects to the game-object
    game.set_screen(screen)
    game.set_background(background)
    game.set_clock(clock)
    game.set_fps(FPS)

    # Initialize the pymunk space
    space = pymunk.Space()
    game.set_space(space)

    # Add post-collision handlers to the space
    # NOTE: In these, we can e.g. play collision sounds, reset jumping flags...
    space.add_collision_handler(col_call.PLAYER_TYPE, col_call.STATIC_TYPE,
                                post_solve=col_call.player_static)
    space.add_collision_handler(col_call.PLAYER_TYPE, col_call.MOVING_TYPE,
                                post_solve=col_call.player_static)

    # Initialize Sprite Groups
    all_sprites = pygame.sprite.LayeredDirty()
    game.set_sprite_group(all_sprites)

    # Handle the objects from the YAML-file
    for key in item_dict:
        if key == 'background':
            pass
        elif key == 'background_file':
            pass
        else:
            for item in item_dict[key]:
                if key == 'static_objects':
                    # All static objects should be added to the space and the game
                    space.add(item.get_shape())
                    game.add_static_objects(item)
                elif key == 'moving_objects':
                    # All moving objects should be added to the space,
                    # the game and the sprite group
                    space.add(item.get_body(), item.get_shape())
                    game.add_moving_objects(item)
                    all_sprites.add(item)
                elif key == 'player':
                    # Add the player to the game
                    space.add(item.get_object().get_body(),
                              item.get_object().get_shape())
                    game.set_player(item)
                    all_sprites.add(item.get_object())
                elif key == 'music':
                    # Extract the info
                    music_file = item['file']
                    vol = item['vol']
                elif key == 'gravity':
                    # Set the gravity of the level
                    space.gravity = item
                else:
                    # Something unknown encountered, print an error and ignore
                    print ('Unknown object found when loading menu: ',
                           item, ', with key: ', key)

    # Define the background for the sprite group
    all_sprites.clear(screen, background)

    # Clear the screen and hide the cursor
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.mouse.set_visible(False)

    # Start the music
    if music_file is not None:
        full_music_file = os.path.join('sound', 'sound_data', music_file)
        pygame.mixer.music.load(full_music_file)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(-1)

    return game


def load_pop_up_menu(screen, file_name):
    '''
    Loads the pop-up menu defined in the YAML-file named "file_name".
    '''
    # Get the full relative path of the YAML-file
    fullname = os.path.join('menu', 'menu_files', file_name)

    # Load the YAML-file
    with open(fullname, 'r') as stream:
        item_dict = yaml.load(stream)

    # Create a background
    background_image_file = item_dict['background_file']
    background_color = item_dict['background']
    width, height = item_dict['background_size']
    pos = item_dict['background_pos']

    if background_image_file is not None:
        background = pygame.transform\
            .smoothscale(view.load_image(background_image_file),
                         (width, height))
    else:
        background = pygame.Surface([width, height])
        background.fill(background_color)

    # Create lists for storing buttons and all objects that should be drawn
    buttons = []
    objs = []

    # Handle the objects from the YAML-file
    for key in item_dict:
        if key == 'background':
            pass
        elif key == 'background_file':
            pass
        elif key == 'background_size':
            pass
        elif key == 'background_pos':
            pass
        else:
            for item in item_dict[key]:
                if key == 'buttons':
                    buttons.append(item)
                    objs.append(item)
                elif key == 'textboxes':
                    objs.append(item)
                elif key == 'music':
                    music_file = item['file']
                    vol = item['vol']
                else:
                    # Something unknown encountered, print an error and ignore
                    print ('Unknown object found when loading menu: ',
                           item, ', with key: ', key)

    # Create a Sprite group for the objects
    obj_group = pygame.sprite.LayeredDirty(*objs)
    # Set the background of the Sprite group
    background_rect = background.get_rect(center=pos)
    obj_group.clear(screen, background)

    # Blit background to screen, set mouse to visible
    # screen.blit(background, background_rect)
    pygame.mouse.set_visible(True)

    pygame.display.flip()

    # Start the music
    # TODO: Find a way to not restart the music if the currently
    #       playing file is to be loaded.
    # TODO: Add smooth fading between songs.
    if music_file is not None:
        full_music_file = os.path.join('sound', 'sound_data', music_file)
        pygame.mixer.music.load(full_music_file)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(-1)

    return buttons, obj_group, background
