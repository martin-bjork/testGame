import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self, text, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self._pos = (x_pos, y_pos)
        self._text = text

        self._text_color = (0, 0, 0, 1)
        # If set to None, the background is transparent
        self._background_color = (150, 150, 150, 1)

        font = pygame.font.Font(None, 50)
        self._text_object = font.render(self._text, True, self._text_color,
                                        self._background_color)
        self._rect = self._text_object.get_rect(center=self._pos)

    def pressed(self, mouse_pos):
        if self._rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    # Getters/Setters

    def get_pos(self):
        return self._pos

    def get_text(self):
        return self._text

    def get_text_color(self):
        return self._text_color

    def get_background_color(self):
        return self._background_color

    def get_text_object(self):
        return self._text_object

    def get_rect(self):
        return self._rect
