"""
Application: Agent Simulation
Author: Roy Burgess
Date : 09/07/2023
"""

import pygame as pg
from pygame.locals import *
import os
import sys
from random import randint
import sim_resource
import wall as w
import agent as ag

class Simulation:
    """Class which describes the simulation and contains the main loop."""
    def __init__(self):
        # Set window to the centre of the screen
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        # Initialise pg
        pg.init()

        # Set the display
        self.SCREEN_RES = (640, 480)
        pg.display.set_caption("Agent Simulation")
        self.surfaceWindow = pg.display.set_mode(self.SCREEN_RES)

        self.clock = pg.time.Clock()

        # Set rect size
        self.SIZE = 10

        # Define colours
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0,255,0)
        self.GREY = (100, 100, 100)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255,255,255)

        self.player_speed = 2
        self.agent_speed = 1
        self.agent_force = 0.4

        self.vec = pg.math.Vector2

        self.sprites = pg.sprite.Group()
        # Add walls
        self.walls = []
        self.walls.append(w.Wall((100,100),(10,100),self.GREY,"Wall"))
        self.walls.append(w.Wall((200,100),(100,10),self.GREY, "Wall"))
        self.walls.append(w.Wall((540,100),(10,100),self.GREY, "Wall"))
        self.walls.append(w.Wall((0,240),(20,20),self.WHITE, "WB"))
        
        # Add Resource
        self.resourceses = []
        for i in range(0, 4):
            self.resourceses.append(sim_resource.Resource((randint(0,self.SCREEN_RES[0]-10),randint(0,self.SCREEN_RES[1]-10)),self.SIZE,self.GREEN,5))

        # Add agents
        self.agents = []
        for i in range(0,10):
            self.agents.append(ag.Agent(self.vec(320,240),self.SIZE,self.YELLOW,self.agent_speed,self.agent_force,"Wander",self.SCREEN_RES,"Grazer",self.walls[3].rect.center))
            self.agents.append(ag.Agent(self.vec(1,240),self.SIZE,self.BLUE,self.agent_speed,self.agent_force,"Wander",self.SCREEN_RES,"Worker",self.walls[3].rect.center))

        

    def run(self):
        showVectors = True
        
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == KEYUP:
                    # Quit using the escape key
                    if event.key == K_ESCAPE:
                        pg.quit()
                        sys.exit()

            # Player keyboard controlls
            key = pg.key.get_pressed()
            
            if key[pg.K_v]:
                showVectors = not showVectors

            # Draw surface
            self.surfaceWindow.fill(self.BLACK)

            # Place resorce
            if len(self.resourceses) < 4:
                self.resourceses.append(sim_resource.Resource((randint(0,self.SCREEN_RES[0]-10),randint(0,self.SCREEN_RES[1]-10)),self.SIZE,self.GREEN,5))
            for resource in self.resourceses:
                if resource.number > 0:
                    pg.draw.rect(self.surfaceWindow, resource.colour, resource.rect)
                else:
                    self.resourceses.remove(resource)

            # Spawn Grazer
            grazerCount = 0
            for agent in self.agents:
                if agent.type == "Grazer":
                    grazerCount += 1
            if grazerCount == 0:
                for i in range(0,4):
                    
                    self.agents.append(ag.Agent(self.vec(320,240),self.SIZE,self.YELLOW,self.agent_speed,self.agent_force,"Wander",self.SCREEN_RES,"Grazer",""))

            # Move agent
            for agent in self.agents:
                if agent.state == "Wander":
                    agent.wander()
                elif agent.state == "Dead":
                    self.agents.remove(agent)
                elif agent.state == "Arrive":
                    agent.arrive(self.walls[3].rect.center)
                
                agent.detect_collision(self.agents)
                agent.detect_collision(self.resourceses)
                agent.detect_collision(self.walls)
                agent.sense(self.agents)
                agent.sense(self.resourceses)
                pg.draw.rect(self.surfaceWindow, agent.colour, agent.rect)
                
                # Draw walls
                for wall in self.walls:
                    pg.draw.rect(self.surfaceWindow, wall.colour,wall.rect)

                if showVectors:
                    #Show_Vectors(agent)
                    scale = 25
                    # current velocity
                    pg.draw.line(self.surfaceWindow, self.GREEN, agent.pos, (agent.pos + agent.vel * scale), 2)
                    # desired
                    pg.draw.line(self.surfaceWindow, self.RED, agent.pos, (agent.pos + agent.desired * scale), 2)

            pg.display.update()
            self.clock.tick(60)
