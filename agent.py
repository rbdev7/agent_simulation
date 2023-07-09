"""
Application: Agent Simulation
Author: Roy Burgess
Date : 09/07/2023
"""

import pygame as pg
from random import randint, uniform
from operator import sub

vec = pg.math.Vector2

WANDER_CIRCLE_DIST = 150
WANDER_CIRCLE_RADIUS = 50
ARRIVE_RADIUS = 50
FLEE_DISTANCE = 50

class Agent(pg.sprite.Sprite):
    """Class to describe an agent."""
    def __init__(self, pos, size, colour, speed, force, state, bounds, type,wb):
        self.pos = pos
        self.size = size
        self.colour = colour
        self.max_speed = speed
        self.max_force = force
        self.acceleration = vec(0, 0)
        self.vel = vec(1, 0).rotate(uniform(0, 360))
        self.rect = pg.Rect(pos,(size,size))
        self.state = state
        self.bounds = bounds
        self.type = type
        self.wb = wb

    def seek(self, target):
        self.desired = tuple(map(sub,target,self.pos))
        self.desired = vec(self.desired)
        self.desired = self.desired.normalize() * self.max_speed
        steer = (self.desired - self.vel)
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        self.acceleration += steer
        self.update()

    def arrive(self, target):
        self.desired = tuple(map(sub,target,self.pos))
        self.desired = vec(self.desired)
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < ARRIVE_RADIUS:
            self.desired *= dist / ARRIVE_RADIUS * self.max_speed
        else:
            self.desired *= self.max_speed
        steer = (self.desired - self.vel)
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        self.acceleration += steer
        self.update()

    def flee(self, target):
        # Create a new vector from the target to overcome the vector subtraction
        # problem.
        d = vec(target[0], target[1])
        dist = (self.pos - d)
        if dist.length() < FLEE_DISTANCE and dist.length() > 0:
            self.desired = dist.normalize() * self.max_speed
        else:
            self.desired = self.vel.normalize() * self.max_speed
        steer = (self.desired - self.vel)
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        self.acceleration += steer
        self.update()

    def wander(self):
        future = self.pos + self.vel.normalize() * WANDER_CIRCLE_DIST
        target = future + vec(WANDER_CIRCLE_RADIUS, 0).rotate(uniform(0, 360))
        self.seek(target)

    def sense(self, things):
        for thing in things:
            if not thing == self:
                if thing.type == "Worker" and self.type == "Grazer":
                    dist = (self.rect.center + vec(FLEE_DISTANCE,FLEE_DISTANCE)) - (thing.rect.center + vec(FLEE_DISTANCE,FLEE_DISTANCE))
                    if dist.length() < FLEE_DISTANCE:
                        self.state = "Flee"
                        self.flee(thing.rect.center)
                    else:
                        self.state = "Wander"
                if thing.type =="Resource":
                    if self.type == "Worker" or self.type == "Grazer":
                        dist = (self.rect.center + vec(FLEE_DISTANCE,FLEE_DISTANCE)) - (thing.rect.center + vec(FLEE_DISTANCE,FLEE_DISTANCE))
                        if dist.length() < 50:
                            self.seek(thing.pos)
                    
    def detect_collision(self, obsticles):
        for obsticle in obsticles:
            if self != obsticle and self.rect.colliderect(obsticle.rect):
                if obsticle.type == "Grazer" and self.type == "Worker":
                    obsticle.state = "Dead"
                elif obsticle.type == "Resource":
                    obsticle.number -= 1
                    if self.type == "Grazer":
                        self.flee(obsticle.rect.center)
                    elif self.type == "Worker":
                        self.target = self.wb
                        self.arrive(self.wb)
                        self.state = "Arrive"
                elif obsticle.type == "WB" and self.type == "Worker":
                    self.target = None
                    self.state = "Wander"
                else:
                    if self.acceleration.x > 0:
                        self.rect.right = obsticle.rect.left
                    if self.acceleration.x < 0:
                        self.rect.left = obsticle.rect.right
                    if self.acceleration.y > 0:
                        self.rect.bottom = obsticle.rect.top
                    if self.acceleration.y < 0:
                        self.rect.top = obsticle.rect.bottom
                    self.pos = self.rect.center

    def update(self):
        self.vel += self.acceleration
        if self.acceleration.length() == 0:
            self.vel.scale_to_length(self.max_speed)
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        self.pos += self.vel

        # Update the rectangle position
        self.rect.center = self.pos

        # Keep the agent within the window
        if self.rect.right > self.bounds[0]:
            self.rect.right = self.bounds[0]
            self.pos = self.rect.center
        if self.rect.left <= 0:
            self.rect.left = 1
            self.pos = self.rect.center
        if self.rect.bottom > self.bounds[1]:
            self.rect.bottom = self.bounds[1]
            self.pos = self.rect.center
        if self.rect.top <= 0:
            self.rect.top = 1
            self.pos = self.rect.center
        