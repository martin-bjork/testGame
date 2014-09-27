import pygame
import yaml
import buttons

pygame.init()

# Create a new Button instance
b = buttons.Button('Hello', 1, 2)
print 'Button: ', b

# Create a YAML-representation of the Button
y = yaml.dump(b)
print '\nYAML: \n', y

# Retrieve a new Button from the YAML-representation
c = yaml.load(y)
print 'New button: ', c
