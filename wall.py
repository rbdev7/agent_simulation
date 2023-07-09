"""
Application: Agent Simulation
Author: Roy Burgess
Date : 09/07/2023
"""

import pygame

class Wall(object):
    """Class to describe a wall obstical."""
    def __init__(self, pos, size, colour, type):
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.colour = colour
        self.type = type
