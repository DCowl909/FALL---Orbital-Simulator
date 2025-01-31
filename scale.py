from constants import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from camera import *
import pygame

class Scale():
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera
        self.font = pygame.font.Font(None, 24)  # Default font, size 24
        pass
    
    def update(self):
        padding = 50
        
        # Render the text
        text = f"0KM                                   {self.camera.scale*200/1000}km"
        text_surface = self.font.render(text, True, WHITE)  # White text
        text_width, text_height = text_surface.get_size()
        self.screen.blit(text_surface, (0+padding, SCREEN_HEIGHT - padding/1.5))
        
        pygame.draw.line(self.screen, WHITE, (0+padding, SCREEN_HEIGHT - padding), (200+padding, SCREEN_HEIGHT - padding), width=4)


