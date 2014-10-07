import pygame
import yaml


class MenuItem(pygame.sprite.Sprite):
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

    def set_background_color(self, color):
        # TODO: Re-render the text object
        self._background_color = color

    # TODO: Add getters/setters for font properties


class Button(MenuItem, yaml.YAMLObject):

    yaml_tag = '!Button'

    def __init__(self, text, x_pos, y_pos):

        MenuItem.__init__(self, text, x_pos, y_pos)

        self._action = None         # A function the Button
                                    # should call when activated
        self._action_args = None    # The arguments needed for the
                                    # function that is called when activated

    @classmethod
    def from_yaml(cls, loader, node):
        '''A constructor that YAML uses to create instances of this class'''
        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        text = values['text']
        pos = values['pos']
        action = values['action']
        action_args = values['action_args']

        # Create an instance of the object
        m = Button(text, pos[0], pos[1])
        m.set_action(action)
        m.set_action_args(action_args)

        # Return the object
        return m

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''A method used by YAML to represent an instance of this class'''
        # Construct a dict containing only the properties (wrong word...)
        # we want to use in the representation
        mapping = {'text': instance._text,
                   'pos': instance._pos,
                   'action': instance._action,
                   'action_args': instance._action_args}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)

    def perform_action(self):
        if self._action_args is not None:
            return self._action(*self._action_args)
        else:
            return self._action()

    def pressed(self, mouse_pos):
        if self._rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    # Getters/setters

    def set_action(self, action):
        self._action = action

    def set_action_args(self, action_args):
        self._action_args = action_args

    def get_action(self):
        return self._action

    def get_action_args(self):
        return self._action_args


class TextBox(MenuItem, yaml.YAMLObject):

    yaml_tag = '!TextBox'

    def __init__(self, text, x_pos, y_pos):

        # FIXME: Text boxes currently doesn't support
        # newlines, this must be fixed!

        MenuItem.__init__(self, text, x_pos, y_pos)

    @classmethod
    def from_yaml(cls, loader, node):
        '''A constructor that YAML uses to create instances of this class'''
        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        text = values['text']
        pos = values['pos']

        # Create an instance of the object
        m = TextBox(text, pos[0], pos[1])

        # Return the object
        return m

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''A method used by YAML to represent an instance of this class'''
        # Construct a dict containing only the properties
        # we want to use in the representation
        mapping = {'text': instance._text,
                   'pos': instance._pos}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)
