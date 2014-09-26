import pygame
import yaml

class Button(pygame.sprite.Sprite, yaml.YAMLObject):

    # The tag that YAML will use to identify this class
    yaml_tag = '!Button'
    # Tells YAML to use the safe loader so others can't execute 
    # code through our code (not quite working yet)
    #yaml_loader = yaml.SafeLoader

    @staticmethod
    def yaml_constructor(loader, node):
        '''A constructor that YAML uses to create instances of this class'''
        # Create a dict from the YAML code for the object,
        # containing all its variables (wrong word...)
        values = loader.construct_mapping(node)
        # Extract the needed variables
        text = values['_text']
        pos = values['_pos']
        # Return a new instance of the object
        return Button(text, pos[0], pos[1])

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
