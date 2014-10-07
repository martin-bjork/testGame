def pymunk_to_pygame_coords(x, y, screen_height):
    return int(x), int(screen_height - y)


def pygame_to_pymunk_coords(x, y, screen_height):
    return x, -y - screen_height
