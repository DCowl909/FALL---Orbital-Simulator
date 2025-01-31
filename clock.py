import pygame
from constants import *
import time


class Clock():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)  # Use PyGame's default font, size 24
        self.padding = 10
        self.simSpeed = 1
        self.simulation_time = pygame.time.get_ticks()/1000  # Real-time tracking
        self.update_clock(0)

    def update_clock(self, time: int):
        #Adjust new text
        text = f"Sim Speed: {self.simSpeed:.1f} | Seconds {int(time)} | Hours {time/3600:.1f} | Days {time/86400:.1f}"
        
        text_surface = self.font.render(text, True, BLACK)  # Create the text surface
        text_width, text_height = text_surface.get_size()  # Get text size

        clock_width = text_width + 2 * self.padding
        clock_height = text_height + 2 * self.padding
        x = SCREEN_WIDTH - clock_width
        y = SCREEN_HEIGHT - clock_height
         
        pygame.draw.rect(self.screen, SPACE_BLUE, (x, y, clock_width, clock_height))
        self.screen.blit(text_surface, (x + self.padding, y + self.padding))
        
    def calculate_sim_speed(self, timePerFrame):
        #to be called every 10 frames
        new = pygame.time.get_ticks()/1000
        d = new - self.simulation_time
        if (d>0):
            self.simSpeed = 10 * timePerFrame/(d)
        self.simulation_time = new
        

        
        