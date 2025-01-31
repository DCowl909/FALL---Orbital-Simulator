import pygame, math, random
import numpy as np
from constants import G, DEFAULT_RADIUS, DEFAULT_MASS
from camera import *

class Body(pygame.sprite.Sprite):
    number = 0
    
    def __init__(self, motionState: np.array, group: pygame.sprite.Group, screen: pygame.Surface, camera: Camera):
        super(Body, self).__init__()
        self.motionState = motionState
        self.group = group
        self.screen = screen
        self.camera = camera
        self.radius = DEFAULT_RADIUS
        self.mass = DEFAULT_MASS 
        
        self.locked = False
        
        self.color = (
            random.randint(50, 255),  # Random Red value
            random.randint(50, 255),  # Random Green value
            random.randint(50, 255)   # Random Blue value
        )
        
        
        #id so can be removed
        self.id = Body.number
        Body.number += 1 
        
    def draw_body(self):
        x, y = self.camera.frame_coordinates(self.motionState[0]) # Extract the center coordinates
        pygame.draw.circle(self.screen, self.color, (int(x), int(y)), self.radius / self.camera.scale)
        
    def contains_frame_point(self, point) -> bool:
        mousePointInSpace = self.camera.space_coordinates(point)
        
        d = math.sqrt(pow(self.motionState[0][0] - mousePointInSpace[0], 2) + pow(self.motionState[0][1] - mousePointInSpace[1], 2))
        if d < self.radius:
            print(f"Click was inside body {self.id}")
            return True
        return False
    
    def set_mass(self, mass):
        self.mass = mass
        #self.radius = math.sqrt(mass)
        pass
    
    def set_radius(self, radius):
        self.radius = radius
        
    def lock_body(self):
        self.locked = True
        self.motionState[1][0] = 0
        self.motionState[1][1] = 0
    
    def acting_acceleration(self, actingBody):
        dpos = actingBody.motionState[0] - self.motionState[0]
        r = math.sqrt(pow(dpos[0], 2) + pow(dpos[1], 2))
        FMag = (G * actingBody.mass) / pow(r, 3)
        return FMag * dpos