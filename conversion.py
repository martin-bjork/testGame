# Conversion functions between pygame and pymunk coordinates.

# TODO: Make the connection between pygame and pymunk coordinates looser
#       so it's possible to have a moving camera to view the world.
# TODO: Use pygame.display.height (or whatever way you retrieve the height
#       of the screen) instead of passing the screen height as an argument.
# TODO: Use pos tuple instead of x and y ints.


def pymunk_to_pygame_coords(x, y, screen_height):
    '''
    A function to convert from pymunk to pygame coordintes.

    Input:
        * x: Float
            - The x-coordinate in pymunk.
        * y: Float
            - The y-coordinate in pymunk.
        * screen_height: Int
            - The height of the screen in pixels.
    Output:
        * pos: 2-tuple of ints
            - The pygame coordinates corresponding to the input.
    '''

    return int(x), int(screen_height - y)


def pygame_to_pymunk_coords(x, y, screen_height):
    '''
    A function to convert from pygame to pymunk coordintes.

    Input:
        * x: Int
            - The x-coordinate in pygame.
        * y: Int
            - The y-coordinate in pygame.
        * screen_height: Int
            - The height of the screen in pixels.
    Output:
        * pos: 2-tuple of ints
            - The pymunk coordinates corresponding to the input.
    '''

    return x, -y - screen_height
