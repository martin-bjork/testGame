from __future__ import division

BASE_TYPE = 0
STATIC_TYPE = 1
MOVING_TYPE = 2
PLAYER_TYPE = 3


def player_static(space, arbiter):

    # NOTE: A hack to be able to access the player object here,
    # not sure if best method...
    for shape in arbiter.shapes:
        if shape.collision_type == PLAYER_TYPE:
            player = shape.player

    player.set_jumping(False)

    # Play bounce sound depending on collision impulse
    if arbiter.is_first_contact:
        impulse = arbiter.total_impulse.get_length()
        player.play_bounce(impulse/1000)


def player_moving(space, arbiter):
    # NOTE: Currently, this is identical to the above function...

    # NOTE: A hack to be able to access the player object here,
    # not sure if best method...
    for shape in arbiter.shapes:
        if shape.collision_type == PLAYER_TYPE:
            player = shape.player

    player.set_jumping(False)

    # Play bounce sound depending on collision impulse
    if arbiter.is_first_contact:
        impulse = arbiter.total_impulse.get_length()
        player.play_bounce(impulse/1000)


def moving_static(space, arbiter):
    pass
