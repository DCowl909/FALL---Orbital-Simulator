import pygame
from constants import *

class Pauser:
    def __init__(self, screen: pygame.Surface):

        self.screen = screen
        self.color = WHITE
        self.triangle_size = TRIANGLE_SIZE
        self.pause_width = PAUSE_WIDTH
        self.pause_height = PAUSE_HEIGHT
        self.padding = 10
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

    def update(self):
        """Draws the backward triangle, pause button, and forward triangle at the bottom center of the screen."""
        # Calculate positions
        center_x = self.screen_width // 2
        bottom_y = self.screen_height - self.triangle_size - self.padding

        # Backward triangle
        backward_triangle = [
            (center_x  - self.padding, bottom_y + self.triangle_size),
            (center_x - self.padding, bottom_y),
            (center_x - self.triangle_size - self.padding, bottom_y + 0.5*self.triangle_size)
        ]
        self.backwardTriangle = pygame.draw.polygon(self.screen, self.color, backward_triangle)

        # Forward triangle
        forward_triangle = [
            (center_x + self.padding, bottom_y + self.triangle_size),
            (center_x + self.padding, bottom_y),
            (center_x + self.triangle_size + self.padding, bottom_y + 0.5*self.triangle_size)
        ]
        self.forwardTriangle = pygame.draw.polygon(self.screen, self.color, forward_triangle)
        
    def in_forward_arrow(self, pos):
        if (self.forwardTriangle.collidepoint(pos)):
            return True
        return False
    
    def in_backward_arrow(self, pos):
        if (self.backwardTriangle.collidepoint(pos)):
            return True
        return False
            
            
 