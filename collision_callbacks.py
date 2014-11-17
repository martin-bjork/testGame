# Callback functions for collisions between objects.
# They determine what will happen when two objects collide with each other
# (apart from the actual collision handling - that is taken care of by the
# physics engine). Things that can be treated here is for example
# playing sound, health calculations etc.

from __future__ import division

# Define different collision types
BASE_TYPE = 0
STATIC_TYPE = 1
MOVING_TYPE = 2
PLAYER_TYPE = 3


def player_static(space, arbiter):
    '''
    Collision callback for collisions between the player and a static object.

    Input:
        * space: pymunk.Space
            - The pymunk Space that the objects live in.
        * arbiter: pymunk.Arbiter
            - A pymunk Arbiter containing the information about the collision.
    '''

    # NOTE: A hack to be able to access the player object here,
    # not sure if best method...
    for shape in arbiter.shapes:
        if shape.collision_type == PLAYER_TYPE:
            player = shape.player

    # Reset the "jump" parameter for the player so it can jump again.
    player.set_jumping(False)

    # Play bounce sound with volume determined by collision impulse strength.
    if arbiter.is_first_contact:
        impulse = arbiter.total_impulse.get_length()
        player.play_bounce(impulse/1000)


def player_moving(space, arbiter):
    '''
    Collision callback for collisions between the player and a moving object.

    Input:
        * space: pymunk.Space
            - The pymunk Space that the objects live in.
        * arbiter: pymunk.Arbiter
            - A pymunk Arbiter containing the information about the collision.
    '''

    # NOTE: Currently, this is identical to the above function...

    # NOTE: A hack to be able to access the player object here,
    # not sure if best method...
    for shape in arbiter.shapes:
        if shape.collision_type == PLAYER_TYPE:
            player = shape.player

    # Reset the "jump" parameter for the player so it can jump again.
    player.set_jumping(False)

    # Play bounce sound with volume determined by collision impulse strength.
    if arbiter.is_first_contact:
        impulse = arbiter.total_impulse.get_length()
        player.play_bounce(impulse/1000)


def moving_static(space, arbiter):
    '''
    Collision callback for collisions between a static and a moving object.

    Input:
        * space: pymunk.Space
            - The pymunk Space that the objects live in.
        * arbiter: pymunk.Arbiter
            - A pymunk Arbiter containing the information about the collision.
    '''

    pass
