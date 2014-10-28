import pygame
import yaml

import view


class MenuItem(pygame.sprite.Sprite):
    '''
    An abstract base class for menu items, such as buttons, text areas etc
    '''

    def __init__(self, text='Default', x_pos=1, y_pos=1,
                 text_color=(0, 0, 0, 1),
                 background_color=(150, 150, 150, 1),
                 background_file=None,
                 scale=1,
                 font_size=20, font_file=None):

        pygame.sprite.Sprite.__init__(self)
        self._pos = (x_pos, y_pos)
        self._text = text

        self._text_color = text_color
        self._background_color = background_color     # None -> transparent
        self._backgound_file = background_file
        self._scale = scale

        self._font_size = font_size
        # A file describing the font (e.g. *.ttf), None -> default
        self._font_file = font_file
        font_obj = pygame.font.Font(font_file, font_size)

        if background_file is not None:
            text_obj = font_obj.render(self._text, True,
                                       self._text_color)
            width, height = text_obj.get_size()
            self.image = pygame.transform\
                .scale(view.load_image(background_file),
                       (int(width*scale), int(height*scale)))
            self.rect = self.image.get_rect(center=self._pos)
            self.image.blit(text_obj, (int(width*(scale-1)*0.5),
                            int(height*(scale-1)*0.5)))

        else:
            self.image = font_obj.render(self._text, True,
                                         self._text_color,
                                         self._background_color)
            self.rect = self.image.get_rect(center=self._pos)

    # Getters/setters

    def get_pos(self):
        return self._pos

    def get_text(self):
        return self._text

    def get_text_color(self):
        return self._text_color

    def get_background_color(self):
        return self._background_color

    def get_font_size(self):
        return self._font_size

    def get_font_file(self):
        return self._font_file

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

    def set_font_size(self, font_size):
        # TODO: Re-render the text object
        self._font_size = font_size

    def set_font_file(self, font_file):
        # TODO: Re-render the text object
        self._font_file = font_file


class Button(MenuItem, yaml.YAMLObject):

    yaml_tag = '!Button'

    def __init__(self, text='Button', x_pos=1, y_pos=1,
                 text_color=(0, 0, 0, 1),
                 background_color=(150, 150, 150, 1),
                 background_file=None,
                 scale=1,
                 font_size=50, font_file=None,
                 action=None, action_args=None):

        MenuItem.__init__(self, text=text, x_pos=x_pos, y_pos=y_pos,
                          text_color=text_color,
                          background_color=background_color,
                          background_file=background_file,
                          scale=scale,
                          font_size=font_size,
                          font_file=font_file)

        # A function the Button should call when activated
        self._action = action
        # The arguments needed for the function that is called when activated
        self._action_args = action_args

    @classmethod
    def from_yaml(cls, loader, node):
        '''A constructor that YAML uses to create instances of this class'''
        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        text = values['text']
        pos = values['pos']
        text_color = values['text_color']
        background_color = values['background_color']
        background_file = values['background_file']
        scale = values['scale']
        font_size = values['font_size']
        font_file = values['font_file']
        action = values['action']
        action_args = values['action_args']

        # Return an instance of the object
        return cls(text=text, x_pos=pos[0], y_pos=pos[1],
                   text_color=text_color,
                   background_color=background_color,
                   background_file=background_file,
                   scale=scale,
                   font_size=font_size,
                   font_file=font_file,
                   action=action,
                   action_args=action_args)

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''A method used by YAML to represent an instance of this class'''
        # Construct a dict containing only the properties (wrong word...)
        # we want to use in the representation
        mapping = {'text': instance._text,
                   'pos': instance._pos,
                   'text_color': instance._text_color,
                   'background_color': instance._background_color,
                   'background_file': instance._backgound_file,
                   'scale': instance._scale,
                   'font_size': instance._font_size,
                   'font_file': instance._font_file,
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
        if self.rect.collidepoint(mouse_pos):
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

    def __init__(self, text='Button', x_pos=1, y_pos=1,
                 text_color=(0, 0, 0, 1),
                 background_color=(150, 150, 150, 1),
                 background_file=None,
                 scale=1,
                 font_size=20, font_file=None):

        # FIXME: Text boxes currently doesn't support
        # newlines, this must be fixed!

        MenuItem.__init__(self, text=text, x_pos=x_pos, y_pos=y_pos,
                          text_color=text_color,
                          background_color=background_color,
                          background_file=background_file,
                          scale=scale,
                          font_size=font_size,
                          font_file=font_file)

    @classmethod
    def from_yaml(cls, loader, node):
        '''A constructor that YAML uses to create instances of this class'''
        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        text = values['text']
        pos = values['pos']
        text_color = values['text_color']
        background_color = values['background_color']
        background_file = values['background_file']
        scale = values['scale']
        font_size = values['font_size']
        font_file = values['font_file']

        # Return an instance of the object
        return cls(text=text, x_pos=pos[0], y_pos=pos[1],
                   text_color=text_color,
                   background_color=background_color,
                   background_file=background_file,
                   scale=scale,
                   font_size=font_size,
                   font_file=font_file)

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''A method used by YAML to represent an instance of this class'''
        # Construct a dict containing only the properties
        # we want to use in the representation
        mapping = {'text': instance._text,
                   'pos': instance._pos,
                   'text_color': instance._text_color,
                   'background_color': instance._background_color,
                   'background_file': instance._backgound_file,
                   'scale': instance._scale,
                   'font_size': instance._font_size,
                   'font_file': instance._font_file}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)
