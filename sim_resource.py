"""
Application: Agent Simulation
Author: Roy Burgess
Date : 09/07/2023
"""

import pygame as pg

class Resource(object):
    """Class to describe a resource for agents to gather."""

    def __init__(self, pos, size, colour, number):
        self.pos = pos
        self.size = size
        self.colour = colour
        self.rect = pg.Rect(pos,(size,size))
        self.number = number
        self.type = "Resource"
