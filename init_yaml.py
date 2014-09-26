#Initializes YAML by adding the needed constructors

import yaml

import buttons

def init():
	yaml.Loader.add_constructor('!Button', buttons.Button.yaml_constructor)