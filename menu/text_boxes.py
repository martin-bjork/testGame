import yaml

from menu import base_menu_item


class TextBox(base_menu_item.BaseMenuItem, yaml.YAMLObject):

    yaml_tag = '!TextBox'

    def __init__(self, text, x_pos, y_pos):

        # FIXME: Text boxes currently doesn't support
        # newlines, this must be fixed!

        base_menu_item.BaseMenuItem.__init__(self, text, x_pos, y_pos)

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
