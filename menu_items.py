import yaml

import base_menu_item


class MenuItem(base_menu_item.BaseMenuItem, yaml.YAMLObject):

    yaml_tag = '!MenuItem'

    def __init__(self, text, x_pos, y_pos):

        base_menu_item.BaseMenuItem.__init__(self, text, x_pos, y_pos)

        self._action = None         # A function the MenuItem
                                    # should call when activated
        self._action_args = None    # The arguments needed for the
                                    # function that is called when activated

        # # TODO: Implement these
        # self._previous = None       # The menuitem that should be
        #                             # highlighted when pressing "up"
        # self._next = None           # The menuitem that should be
        #                             # highlighted when pressing "down"

    @classmethod
    def from_yaml(cls, loader, node):
        '''A constructor that YAML uses to create instances of this class'''
        # Create a dict from the YAML code for the object,
        # containing all its properties
        values = loader.construct_mapping(node)

        # Extract the needed properties
        text = values['text']
        pos = values['pos']
        # previous = values['previous']
        # nxt = values['next']
        action = values['action']
        action_args = values['action_args']

        # Create an instance of the object
        m = MenuItem(text, pos[0], pos[1])
        # m.set_previous(previous)
        # m.set_next(nxt)
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
                   # 'previous': instance._previous,
                   # 'next': instance._next,
                   'action': instance._action,
                   'action_args': instance._action_args}

        # Use YAMLs default representation, but with the custom YAML-tag
        # and using only the properties in out custom mapping
        return dumper.represent_mapping(cls.yaml_tag, mapping)

    def perform_action(self):
        return self._action(*self._action_args)

    def pressed(self, mouse_pos):
        if self._rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    # Getters/setters

    # def set_previous(self, menuitem):
    #     self._previous = menuitem

    # def set_next(self, menuitem):
    #     self._next = menuitem

    def set_action(self, action):
        self._action = action

    def set_action_args(self, action_args):
        self._action_args = action_args

    # def get_previous(self):
    #     return self._previous

    # def get_next(self):
    #     return self._next

    def get_action(self):
        return self._action

    def get_action_args(self):
        return self._action_args
