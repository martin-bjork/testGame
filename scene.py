# TODO: Add a level constructing function so we don't have to
# hard-code everything
from __future__ import division
import pymunk
import pygame

import players
import shapes
import collision_callbacks as col_call


# TODO: Move these functions to another file
def pymunk_to_pygame_coords(x, y, screen_height):
    return int(x), int(screen_height - y)


def pygame_to_pymunk_coords(x, y, screen_height):
    return x, -y - screen_height


def init_scene(game):

    # Initialize the pymunk space
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    game.set_space(space)

    ### Set up the boundaries of the world
    # TODO: Add level creation here

    width, height = game.get_screen_size()

    # Create a static for the world boundaries
    static_body = pymunk.Body()

    # Create the boundaries
    floor = pymunk.Segment(static_body, (0, 0), (width, 0), 5.0)
    ceiling = pymunk.Segment(static_body, (0, height), (width, height), 5.0)
    right_wall = pymunk.Segment(static_body, (width, 0), (width, height), 5.0)
    left_wall = pymunk.Segment(static_body, (0, 0), (0, height), 5.0)

    # Physical properties of the boundaries
    floor.friction = 1.0
    floor.elasticity = 0.8
    ceiling.friction = 1.0
    ceiling.elasticity = 0.8
    right_wall.friction = 1.0
    right_wall.elasticity = 0.8
    left_wall.friction = 1.0
    left_wall.elasticity = 0.8

    # Set collision types
    # TODO: Move to the constructors of each shape
    floor.collision_type = col_call.STATIC_TYPE
    ceiling.collision_type = col_call.STATIC_TYPE
    right_wall.collision_type = col_call.STATIC_TYPE
    left_wall.collision_type = col_call.STATIC_TYPE

    # Add them to the space and game
    space.add(floor)
    space.add(ceiling)
    space.add(right_wall)
    space.add(left_wall)
    game.add_static_objects(floor, ceiling, right_wall, left_wall)

    # Create the player
    player_pos = (width/2, 30)
    player = players.Player(space, position=player_pos)
    game.set_player(player)

    # Create moving objects
    rect_pos = (width/3, 30)
    block = shapes.Rectangle(space, position=rect_pos, color=(0, 250, 0))
    game.add_moving_objects(block)

    # Initialize Sprite Groups
    # (will be more useful when we have more moving sprites)
    all_sprites = pygame.sprite.RenderUpdates()
    game.set_sprite_group(all_sprites)

    all_sprites.add(player)
    all_sprites.add(block)

    # Start background music
    pygame.mixer.music.load('sound/sound_data/trololo1.wav')
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

    # Add post-collision handlers to the space
    # NOTE: In these, we can e.g. play collision sounds, reset jumping flags...
    space.add_collision_handler(col_call.PLAYER_TYPE, col_call.STATIC_TYPE,
                                post_solve=col_call.player_static)
    space.add_collision_handler(col_call.PLAYER_TYPE, col_call.MOVING_TYPE,
                                post_solve=col_call.player_static)

    return space
