# Functions that handle YAML-files and load menus and levels from them.

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
import cameras

# TODO: Add a "To YAML"-function?
# TODO: Better docstrings


def load_menu(file_name):
    '''
    Loads the menu defined in the YAML-file named "file_name".

    Input:
        * file_name: String
            - The name of the YAML-file describing the menu.
    Output:
        * buttons: List of menu_items.Button
            - A list of all the buttons in the menu.
        * obj_group: pygame.sprite.LayeredDirty
            - A pygame Sprite Group containing the MenuItems in the menu.
        * screen: pygame.Surface
            - The screen of the menu.
        * background: pygame.Surface
            - The background of the menu.
    '''

    # TODO: Remove "screen" from output? It can be referenced
    #       directly via pygame.

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
        background = view.load_and_scale(background_image_file,
                                         (width, height))
    else:
        if len(background_color) == 4:
            # Alpha value specified
            background = pygame.Surface([width, height], pygame.SRCALPHA)
        else:
            # Only RGB specified
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
    # TODO: Add smooth fading between songs.
    if music_file is not None:
        # Get the full relative path of the music file
        full_music_path = os.path.join('sound', 'sound_data', music_file)
        # Get the currently loaded song and whether it's playing
        current_song, playing = pygame.music_player.get_playing()

        if current_song == full_music_path and playing:
            # The right song is already playing; do nothing
            pass
        elif current_song == full_music_path and not playing:
            # The right song is loaded, but not playing; start the song
            pygame.music_player.play()
        else:
            # The wrong song is loaded; load the right one and start it
            pygame.music_player.load_and_play(full_music_path)

        pygame.music_player.set_volume(vol)

    return buttons, obj_group, screen, background


def load_level(file_name):
    '''
    Loads the level defined in the YAML-file named "file_name".

    Output:
        * game: gameclass.Game
            - A Game object containing all info about the level.
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
    # info = pygame.display.Info()
    # width = info.current_w
    # height = info.current_h
    width, height = item_dict['size']
    # screen = pygame.display.get_surface()

    if background_image_file is not None:
        background = view.load_and_scale(background_image_file,
                                         (width, height))
    else:
        if len(background_color) == 4:
            # Alpha value specified
            background = pygame.Surface([width, height], pygame.SRCALPHA)
        else:
            # Only RGB specified
            background = pygame.Surface([width, height])
        background.fill(background_color)

    # Create other game related objects
    FPS = 60
    clock = pygame.time.Clock()
    camera = item_dict['camera']

    # Add the objects to the game-object
    game.set_background(background)
    game.set_clock(clock)
    game.set_fps(FPS)
    game.set_camera(camera)

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
        elif key == 'camera':
            pass
        elif key == 'size':
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

    # Update all moving objects
    all_sprites.update(game)

    # Hide the cursor
    pygame.mouse.set_visible(False)

    # Start the music
    if music_file is not None:
        # Get the full relative path of the music file
        full_music_path = os.path.join('sound', 'sound_data', music_file)
        # Get the currently loaded song and whether it's playing
        current_song, playing = pygame.music_player.get_playing()

        if current_song == full_music_path and playing:
            # The right song is already playing; do nothing
            pass
        elif current_song == full_music_path and not playing:
            # The right song is loaded, but not playing; start the song
            pygame.music_player.play()
        else:
            # The wrong song is loaded; load the right one and start it
            pygame.music_player.load_and_play(full_music_path)

        pygame.music_player.set_volume(vol)

    return game


def load_pop_up_menu(file_name):
    '''
    Loads the pop-up menu defined in the YAML-file named "file_name".

    Input:
        * file_name: String
            - The name of the YAML-file describing the menu.
    Output:
        * buttons: List of menu_items.Button
            - A list of all the buttons in the menu.
        * obj_group: pygame.sprite.LayeredDirty
            - A pygame Sprite Group containing the MenuItems in the menu.
        * background: pygame.Surface
            - The background of the menu.
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
    screen = pygame.display.get_surface()

    if background_image_file is not None:
        background = view.load_and_scale(background_image_file,
                                         (width, height))
    else:
        if len(background_color) == 4:
            # Alpha value specified
            background = pygame.Surface([width, height], pygame.SRCALPHA)
        else:
            # Only RGB specified
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

    # Blit background to screen, set mouse to visible
    background_rect = background.get_rect(center=pos)
    screen.blit(background, background_rect)
    pygame.mouse.set_visible(True)

    # Shift all objects to place them at the pop-up menus position
    for obj in obj_group:
        obj.add_pos(background_rect.topleft)

    pygame.display.flip()

    # Start the music
    # TODO: Find a way to not restart the music if the currently
    #       playing file is to be loaded.
    # TODO: Add smooth fading between songs.
    if music_file is not None:
        # Get the full relative path of the music file
        full_music_path = os.path.join('sound', 'sound_data', music_file)
        # Get the currently loaded song and whether it's playing
        current_song, playing = pygame.music_player.get_playing()

        if current_song == full_music_path and playing:
            # The right song is already playing; do nothing
            pass
        elif current_song == full_music_path and not playing:
            # The right song is loaded, but not playing; start the song
            pygame.music_player.play()
        else:
            # The wrong song is loaded; load the right one and start it
            pygame.music_player.load_and_play(full_music_path)

        pygame.music_player.set_volume(vol)

    return buttons, obj_group, background
