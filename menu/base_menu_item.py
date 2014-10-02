import pygame


class BaseMenuItem(pygame.sprite.Sprite):
    '''
    An abstract base class for menu items, such as buttons, text areas etc
    '''

    def __init__(self, text, x_pos, y_pos):

        pygame.sprite.Sprite.__init__(self)
        self._pos = (x_pos, y_pos)
        self._text = text

        # TODO: Set these via kwargs?
        self._text_color = (0, 0, 0, 1)
        self._background_color = (150, 150, 150, 1)     # None -> transparent

        # TODO: Set these via kwargs too?
        font_size = 50
        font_file = None    # A file describing the font (e.g. *.ttf), None -> default
        font_obj = pygame.font.Font(font_file, font_size)

        self._text_obj = font_obj.render(self._text, True, self._text_color,
                                         self._background_color)
        self._rect = self._text_obj.get_rect(center=self._pos)

    # Getters/setters

    def get_pos(self):
        return self._pos

    def get_text(self):
        return self._text

    def get_text_color(self):
        return self._text_color

    def get_background_color(self):
        return self._background_color

    def get_text_object(self):
        return self._text_obj

    def get_rect(self):
        return self._rect

    def set_pos(self, pos):
        self._pos = pos

    def set_text(self, text):
        # TODO: Re-render the text object
        self._text = text

    def set_text_color(self, color):
        # TODO: Re-render the text object
        self._text_color = color

    def set_beckground_color(self, color):
        # TODO: Re-render the text object
        self._background_color = color

    # TODO: Add getters/setters for font properties
