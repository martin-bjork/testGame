import os

import pygame
import yaml

import view


class MenuItem(pygame.sprite.DirtySprite):
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
    #       Could use both by setting int -> pixels, float -> scaling.

    def __init__(self, text='Default', x_pos=1, y_pos=1,
                 text_color=(0, 0, 0, 1.0),
                 background_color=(255, 255, 255, 1.0),
                 background_file=None,
                 w_scale=1.0, h_scale=1.0,
                 font_size=20, font_file=None):

        # Run the constructor of the Sprite-class that MenuItem inherits from
        pygame.sprite.DirtySprite.__init__(self)

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
        self.dirty = 1

    def render(self):
        '''
        Renders the MenuItem and assigns the Surface and Rect to
        self.image and self.rect.
        Should be called from the constructor, as well as every time
        the MenuItem is altered (e.g. if the text colour is changed).
        '''
        self.image, self.rect = self._render()

    def _render(self):
        '''
        Renders the MenuItem by creating a pygame Surface defined by
        the properties of the MenuItem, and returns this and the
        corresponding pygame Rect.

        Output:
            * image: pygame.Surface
                - The Surface defined by the MenuItems properties.
            * rect: pygame.Rect
                - The Rect correstponding to image
        '''

        # Get the full path of the font file
        if self._font_file is not None:
            font_file = os.path.join('fonts', self._font_file)
        else:
            font_file = None

        # Create a font object from the font file and size
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
            image = pygame.transform\
                .smoothscale(view.load_image(self._background_file),
                             (int(tot_width * self._w_scale),
                              int(tot_height * self._h_scale)))
        else:
            # Create a solid coloured rectangle of the desired size
            image = pygame.Surface((int(tot_width * self._w_scale),
                                    int(tot_height * self._h_scale)))
            image.fill(self._background_color)

        # Get the rect of the background
        rect = image.get_rect(center=self._pos)

        # Blit the text to the background
        for i in range(len(rend_lines)):
            # Calculate the position of the upper left corner of the new line
            y_pos = int(tot_height * (self._h_scale - 1) * 0.5
                        + i * rend_lines[0].get_height())

            x_pos = int(tot_width * (self._w_scale - 1) * 0.5
                        + (tot_width - rend_lines[i].get_width()) * 0.5)

            image.blit(rend_lines[i], (x_pos, y_pos))

        return image, rect

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
        self.dirty = 1

    def set_text(self, text):
        self._text = text
        self.render()
        self.dirty = 1

    def set_text_color(self, color):
        self._text_color = color
        self.render()
        self.dirty = 1

    def set_background_color(self, color):
        self._background_color = color
        self.render()
        self.dirty = 1

    def set_background_file(self, background_file):
        self._background_file = background_file
        self.render()
        self.dirty = 1

    def set_font_size(self, font_size):
        self._font_size = font_size
        self.render()
        self.dirty = 1

    def set_font_file(self, font_file):
        self._font_file = font_file
        self.render()
        self.dirty = 1


class Button(MenuItem, yaml.YAMLObject):
    '''
    A class for buttons: Clickable objects in menus that can execute
    code when clicked.

    Keyword arguments for constructor:
    (Only the ones that differ from the ones described in MenuItem.
     If only the default value is different, no description is added.)
        * text: String
            - Default: 'Button'
        * hov_text: String
            - The text to be displayed on the MenuItem when
              the mouse hovers over it.
            - Default: 'Button'
        * hov_text_color: 3- or 4-tuple of 3 ints and 0 or 1 float
            - The colour of the text in rgb[a] when
              the mouse hovers over it.
              r, g and b are ints 0-255, a is a float 0-1.
            - Default: (0, 0, 0, 1.0)
        * hov_background_color: 3- or 4-tuple of 3 ints and 0 or 1 float
            - The colour of the background in rgb[a] when
              the mouse hovers over it.
              r, g and b are ints 0-255, a is a float 0-1.
              If set to None, the background is transparent.
              If a background image is specified via background_file,
              the background colour will be ignored.
            - Default: (255, 255, 255, 1.0)
        * hov_background_file: String
            - The name of the file of the image to be used as background
              for the MenuItem when the mouse hovers over it.
              If set to None, no image will be used and the MenuItem uses
              a solid background with colour defined by background_color.
            - Default: None
        * font_size: Int
            - Default: 50
        * action: function
            - The function that should be called when clicking the button.
            - Default: None
        * action_args: List
            - A list containing the arguments that should be passed to the
              action function when the button is being clicked.
            - Default: None
    '''

    # NOTE: It is possible that the button might flicker if the size
    #       of the "hovered" rect is smaller than the "unhovered",
    #       since this could lead to that the mouse can hover over
    #       the unhovered rect but not the hovered. This would lead
    #       to that the image for the button would change each frame,
    #       leading to flickering. Until a solution for this has been
    #       found, please try to make sure that the hovered rect is
    #       always equal to or bigger than the unhovered rect.

    yaml_tag = '!Button'

    def __init__(self, text='Button', hov_text='Button', x_pos=1, y_pos=1,
                 text_color=(0, 0, 0, 1.0),
                 hov_text_color=(0, 0, 0, 1.0),
                 background_color=(255, 255, 255, 1.0),
                 hov_background_color=(255, 255, 255, 1.0),
                 background_file=None,
                 hov_background_file=None,
                 w_scale=1.0, h_scale=1.0,
                 font_size=50, font_file=None,
                 action=None, action_args=None):

        # Call the constructor of the superclass
        MenuItem.__init__(self, text=text, x_pos=x_pos, y_pos=y_pos,
                          text_color=text_color,
                          background_color=background_color,
                          background_file=background_file,
                          w_scale=w_scale, h_scale=h_scale,
                          font_size=font_size,
                          font_file=font_file)

        # Store the arguments for later use
        self._action = action
        self._action_args = action_args
        self._hov_text = hov_text
        self._hov_text_color = hov_text_color
        self._hov_background_color = hov_background_color
        self._hov_background_file = hov_background_file

        # Save the image and rect for when the button is not being hovered
        self._base_image = self.image
        self._base_rect = self.rect

        # Create image and rect for when the button is being hovered
        self._text = hov_text
        self._text_color = hov_text_color
        self._background_color = hov_background_color
        self._background_file = hov_background_file

        self._hov_image, self._hov_rect = self._render()

        # Reset the properties
        self._text = text
        self._text_color = text_color
        self._background_color = background_color
        self._background_file = background_file

        self._hovered = False

    @classmethod
    def from_yaml(cls, loader, node):
        '''
        A constructor that YAML uses to create instances of this class.
        '''

        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        text = values['text']
        hov_text = values['hov_text']
        pos = values['pos']
        text_color = values['text_color']
        hov_text_color = values['hov_text_color']
        background_color = values['background_color']
        hov_background_color = values['hov_background_color']
        background_file = values['background_file']
        hov_background_file = values['hov_background_file']
        w_scale = values['w_scale']
        h_scale = values['h_scale']
        font_size = values['font_size']
        font_file = values['font_file']
        action = values['action']
        action_args = values['action_args']

        # Return an instance of the object
        return cls(text=text, hov_text=hov_text, x_pos=pos[0], y_pos=pos[1],
                   text_color=text_color, hov_text_color=hov_text_color,
                   background_color=background_color,
                   hov_background_color=hov_background_color,
                   background_file=background_file,
                   hov_background_file=hov_background_file,
                   w_scale=w_scale,
                   h_scale=h_scale,
                   font_size=font_size,
                   font_file=font_file,
                   action=action,
                   action_args=action_args)

    @classmethod
    def to_yaml(cls, dumper, instance):
        '''
        A method used by YAML to represent an instance of this class.
        '''

        # Construct a dict containing only the properties (wrong word...)
        # we want to use in the representation
        mapping = {'text': instance._text,
                   'hov_text': instance._hov_props['text'],
                   'pos': instance._pos,
                   'text_color': instance._text_color,
                   'hov_text_color': instance._hov_props['text_color'],
                   'background_color': instance._background_color,
                   'hov_background_color': instance._hov_props['background_color'],
                   'background_file': instance._backgound_file,
                   'hov_background_file': instance._hov_props['background_file'],
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
        '''
        Call the function defined by self._action.
        '''

        if self._action_args is not None:
            return self._action(*self._action_args)
        else:
            return self._action()

    def pressed(self, mouse_pos):
        '''
        Check if the point defined by mouse_pos is inside the button.
        '''

        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    # Getters/setters

    def set_action(self, action):
        self._action = action

    def set_action_args(self, action_args):
        self._action_args = action_args

    def set_hovered(self, hovered):
        # TODO: Add docstring
        if hovered != self._hovered:
            self._hovered = hovered
            if self._hovered:
                self.image = self._hov_image
                self.rect = self._hov_rect
            else:
                self.image = self._base_image
                self.rect = self._base_rect
            self.dirty = 1
        else:
            pass

    def set_text(self, text):
        self._text = text
        self._base_image, self._base_rect = self._render()
        self.dirty = 1

    def set_hov_text(self, text):
        self._hov_text = text
        self._hov_image, self._hov_rect = self._render()
        self.dirty = 1

    def set_text_color(self, color):
        self._text_color = color
        self._base_image, self._base_rect = self._render()
        self.dirty = 1

    def set_hov_text_color(self, color):
        self._hov_text_color = color
        self._hov_image, self._hov_rect = self._render()
        self.dirty = 1

    def set_background_color(self, color):
        self._background_color = color
        self._base_image, self._base_rect = self._render()
        self.dirty = 1

    def set_hov_background_color(self, color):
        self._hov_background_color = color
        self._hov_image, self._hov_rect = self._render()
        self.dirty = 1

    def set_background_file(self, background_file):
        self._background_file = background_file
        self._base_image, self._base_rect = self._render()
        self.dirty = 1

    def set_hov_background_file(self, background_file):
        self._hov_background_file = background_file
        self._hov_image, self._hov_rect = self._render()
        self.dirty = 1

    def get_hov_text(self):
        return self._hov_text

    def get_hov_text_color(self):
        return self._hov_text_color

    def get_hov_background_color(self):
        return self._hov_background_color

    def get_hov_background_file(self):
        return self._hov_background_file

    def get_action(self):
        return self._action

    def get_action_args(self):
        return self._action_args

    def get_hovered(self):
        return self._hovered


class TextBox(MenuItem, yaml.YAMLObject):
    '''
    A class for text boxes: Non-interacting rectangles with text.

    Keyword arguments for constructor:
    (Only the ones that differ from the ones described in MenuItem.
     If only the default value is different, no description is added.)
        * text: String
            - Default: 'Text box'
    '''

    yaml_tag = '!TextBox'

    def __init__(self, text='Text box', x_pos=1, y_pos=1,
                 text_color=(0, 0, 0, 1.0),
                 background_color=(255, 255, 255, 1.0),
                 background_file=None,
                 w_scale=1.0, h_scale=1.0,
                 font_size=20, font_file=None):

        MenuItem.__init__(self, text=text, x_pos=x_pos, y_pos=y_pos,
                          text_color=text_color,
                          background_color=background_color,
                          background_file=background_file,
                          w_scale=w_scale, h_scale=h_scale,
                          font_size=font_size,
                          font_file=font_file)

        # Should always be redrawn
        self.dirty = 2

    @classmethod
    def from_yaml(cls, loader, node):
        '''
        A constructor that YAML uses to create instances of this class.
        '''

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
        '''
        A method used by YAML to represent an instance of this class.
        '''

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
