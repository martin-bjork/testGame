# TODO: Add a level constructing function so we don't have to
# hard-code everything
import pymunk


def pymunk_to_pygame_coords(x, y, screen_height):
    return int(x), int(screen_height - y)


def pygame_to_pymunk_coords(x, y, screen_height):
    return x, -y - screen_height


def init_scene(game):

    # Initialize the pymunk space
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

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

    # Add them to the space
    space.add(floor)
    space.add(ceiling)
    space.add(right_wall)
    space.add(left_wall)

    return space
