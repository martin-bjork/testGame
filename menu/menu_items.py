import os

import pygame
import yaml

import view


class MenuItem(pygame.sprite.Sprite):
    '''
    An abstract base class for menu items, such as buttons, text areas etc.
    All other menu item classes inherit from this class.

    Keyword arguments for the constructor:
        * text: String
            - The text to be displayed on the MenuItem.
            - Default: 'Default'
        * x_pos: Int
            - The horizontal position of the center of the MenuItem,
              given in pygame coordinates (pixels from upper left
              corner of window).
            - Default: 1
        * y_pos: Int
            - The vertical position of the center of the MenuItem,
              given in pygame coordinates (pixels from upper left
              corner of window).
            - Default: 1
        * text_color: 3- or 4-tuple of 3 ints and 0 or 1 float
            - The colour of the text in rgb[a].
              r, g and b are ints 0-255, a is a float 0-1.
            - Default: (0, 0, 0, 1.0)
        * background_color: 3- or 4-tuple of 3 ints and 0 or 1 float
            - The colour of the background in rgb[a].
              r, g and b are ints 0-255, a is a float 0-1.
              If set to None, the background is transparent.
              If a background image is specified via background_file,
              the background colour will be ignored.
            - Default: (255, 255, 255, 1.0)
        * background_file: String
            - The name of the file of the image to be used as background
              for the MenuItem.
              If set to None, no image will be used and the MenuItem uses
              a solid background with colour defined by background_color.
            - Default: None
        * w_scale: Float
            - A factor specifying how much wider the background should be
              compared to the text.
            - Default: 1.0
        * h_scale: Float
            - A factor specifying how much higher the background should be
              compared to the text.
            - Default: 1.0
        * font_size: Int
            - The font size of the text in the MenuItem.
            - Default: 20
        * font_file: String
            - The name of the ttf-file defining the font to
              be used in the MenuItem.
              If set to None, it uses pygames default font.
            - Default: None
    '''
    # TODO: Use a tuple for pos instead of two arguments?
    # TODO: Use a tuple for scale instead of two arguments?
    # TODO: Specify padding in pixels instead of a scaling factor?

    def __init__(self, text='Default', x_pos=1, y_pos=1,
                 text_color=(0, 0, 0, 1.0),
                 background_color=(255, 255, 255, 1.0),
                 background_file=None,
                 w_scale=1.0, h_scale=1.0,
                 font_size=20, font_file=None):

        # Run the constructor of the Sprite-class that MenuItem inherits from
        pygame.sprite.Sprite.__init__(self)

        # Store the arguments for later use and to be able to store as YAML
        self._text = text
        self._pos = (x_pos, y_pos)
        self._text_color = text_color
        self._background_color = background_color
        self._background_file = background_file
        self._w_scale = w_scale
        self._h_scale = h_scale
        self._font_size = font_size
        self._font_file = font_file

        # Render the MenuItem
        self.render()

    def render(self):
        '''
        Renders the MenuItem by creating a pygame Surface defined by
        the properties of the MenuItem, and assigning this and the
        corresponding pygame Rect to self.image and self.rect, respectively.
        Should be called from the constructor, as well as every time
        the MenuItem is altered (e.g. if the text colour is changed).
        '''
        if self._font_file is not None:
            font_file = os.path.join('fonts', self._font_file)
        else:
            font_file = None

        font_obj = pygame.font.Font(font_file, self._font_size)

        # Get the individual lines of the text
        lines = self._text.split('\n')
        # Render each line
        rend_lines = [font_obj.render(line, True, self._text_color)
                      for line in lines]

        # Get the width of the longest line
        tot_width = max([line.get_width() for line in rend_lines])
        # Get the total height of the lines
        tot_height = sum([line.get_height() for line in rend_lines])

        # Create a background
        if self._background_file is not None:
            # Load the background image and scale to desired size
            self.image = pygame.transform\
                .smoothscale(view.load_image(self._background_file),
                             (int(tot_width * self._w_scale),
                              int(tot_height * self._h_scale)))
        else:
            # Create a solid coloured rectangle of the desired size
            self.image = pygame.Surface((int(tot_width * self._w_scale),
                                        int(tot_height * self._h_scale)))
            self.image.fill(self._background_color)

        # Get the rect of the background
        self.rect = self.image.get_rect(center=self._pos)

        # Blit the text to the background
        for i in range(len(rend_lines)):
            # Calculate the position of the upper left corner of the new line
            y_pos = int(tot_height * (self._h_scale - 1) * 0.5
                        + i * rend_lines[0].get_height())

            x_pos = int(tot_width * (self._w_scale - 1) * 0.5
                        + (tot_width - rend_lines[i].get_width()) * 0.5)

            self.image.blit(rend_lines[i], (x_pos, y_pos))

    # Getters/setters

    def get_pos(self):
        return self._pos

    def get_text(self):
        return self._text

    def get_text_color(self):
        return self._text_color

    def get_background_color(self):
        return self._background_color

    def get_background_file(self):
        return self._background_file

    def get_font_size(self):
        return self._font_size

    def get_font_file(self):
        return self._font_file

    def set_pos(self, pos):
        self._pos = pos
        self.rect = self.image.get_rect(center=self._pos)

    def set_text(self, text):
        self._text = text
        self.render()

    def set_text_color(self, color):
        self._text_color = color
        self.render()

    def set_background_color(self, color):
        self._background_color = color
        self.render()

    def set_background_file(self, background_file):
        self._background_file = background_file
        self.render()

    def set_font_size(self, font_size):
        self._font_size = font_size
        self.render()

    def set_font_file(self, font_file):
        self._font_file = font_file
        self.render()


class Button(MenuItem, yaml.YAMLObject):

    yaml_tag = '!Button'

    def __init__(self, text='Button', x_pos=1, y_pos=1,
                 text_color=(0, 0, 0, 1),
                 background_color=(150, 150, 150, 1),
                 background_file=None,
                 w_scale=1, h_scale=1,
                 font_size=50, font_file=None,
                 action=None, action_args=None):

        MenuItem.__init__(self, text=text, x_pos=x_pos, y_pos=y_pos,
                          text_color=text_color,
                          background_color=background_color,
                          background_file=background_file,
                          w_scale=w_scale, h_scale=h_scale,
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
        w_scale = values['w_scale']
        h_scale = values['h_scale']
        font_size = values['font_size']
        font_file = values['font_file']
        action = values['action']
        action_args = values['action_args']

        # Return an instance of the object
        return cls(text=text, x_pos=pos[0], y_pos=pos[1],
                   text_color=text_color,
                   background_color=background_color,
                   background_file=background_file,
                   w_scale=w_scale,
                   h_scale=h_scale,
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
                   'w_scale': instance._w_scale,
                   'h_scale': instance._h_scale,
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
                 w_scale=1, h_scale=1,
                 font_size=20, font_file=None):

        MenuItem.__init__(self, text=text, x_pos=x_pos, y_pos=y_pos,
                          text_color=text_color,
                          background_color=background_color,
                          background_file=background_file,
                          w_scale=w_scale, h_scale=h_scale,
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
        w_scale = values['w_scale']
        h_scale = values['h_scale']
        font_size = values['font_size']
        font_file = values['font_file']

        # Return an instance of the object
        return cls(text=text, x_pos=pos[0], y_pos=pos[1],
                   text_color=text_color,
                   background_color=background_color,
                   background_file=background_file,
                   w_scale=w_scale,
                   h_scale=h_scale,
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
                   'w_scale': instance._w_scale,
                   'h_scale': instance._h_scale,
                   'font_size': instance._font_size,
                   'font_file': instance._font_file}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)
