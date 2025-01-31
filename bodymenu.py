import pygame
from constants import *
import math

class BodyMenu():
    def __init__(self, screen):
        self.screen = screen
        self.padding = 10
        self.font = pygame.font.Font(None, 30)  # Use PyGame's default font, size 24
        
        self.body = None #starts as None and then is assigned one by main loop
        self.visible = False #if is visible by user
        self.colour = SPACE_BLUE
        
        self.kinematicRect  = None
        self.massRect = None
        self.lockRect = None
        self.viewRect = False
        
        
        self.massSelected = False
        self.viewSelected = False
        
        
    def set_body(self, body):
        self.body = body
        self.visible = True
        self.colour = body.color
        
    def in_menu(self, pos):
        if (self.in_mass_box(pos) or self.in_kinematic_box(pos) or self.in_lock_box(pos) or self.in_view_box(pos)):
            return True
        return False
    
    def in_kinematic_box(self, pos):
        if (self.kinematicRect.collidepoint(pos)):
            return True
            
    def in_mass_box(self, pos):
        if (self.massRect.collidepoint(pos)):
            return True
        return False
    
    def in_lock_box(self, pos):
        if (self.lockRect.collidepoint(pos)):
            return True
        return False
    
    def in_view_box(self, pos):
        if (self.viewRect.collidepoint(pos)):
            return True
        return False
        
    def hide(self):
        self.visible = False
        self.viewSelected
        

    def update(self):
        if self.visible:
            # Format position, velocity, and acceleration as strings with two decimal points
            pos_str = ", ".join(f"{value:.2f}" for value in self.body.motionState[0])
            vel_str = ", ".join(f"{value:.2f}" for value in self.body.motionState[1])
            acc_str = ", ".join(f"{value:.2f}" for value in self.body.motionState[2])
            absvel = math.sqrt(pow(self.body.motionState[1][0], 2) +pow(self.body.motionState[1][1], 2))
            absacc = math.sqrt(pow(self.body.motionState[2][0], 2) +pow(self.body.motionState[2][1], 2))

            # Kinematic text
            kinematic_text = f"Pos: ({pos_str}), Vel: ({vel_str}) |{absvel:.2f}|, Acc: ({acc_str}) |{absacc:.2f}|"
            kinematic_surface = self.font.render(kinematic_text, True, BLACK)
            kinematic_width, kinematic_height = kinematic_surface.get_size()

            # Mass text
            mass_text = f"Mass: {self.body.mass:.2f}  )"
            mass_surface = self.font.render(mass_text, True, BLACK)
            mass_width, mass_height = mass_surface.get_size()
            
             # Radius text
            rad_text = f"Radius: {self.body.radius:.2f}   "
            radius_surface = self.font.render(rad_text, True, BLACK)
            rad_width, rad_height = radius_surface.get_size()
            
            # Locked Text
            lock_text = "UNLOCK   " if self.body.locked else "LOCK   "
            lock_colour = SOFT_RED if self.body.locked else SOFT_GREEN
            lock_surface = self.font.render(lock_text, True, BLACK)
            lock_width, lock_height = lock_surface.get_size()
            
            #View Text
            view_text = "UNVIEW" if self.viewSelected else "VIEW"
            view_surface = self.font.render(view_text, True, BLACK)
            view_width, view_height = view_surface.get_size()

            # Total height (same for both rectangles)
            height = kinematic_height + 2 * self.padding

            # Background menu box for kinematic text
            self.kinematicRect = pygame.draw.rect(self.screen, self.colour, (0, 0, kinematic_width + 2 * self.padding, height))

            # Draw kinematic text
            self.screen.blit(kinematic_surface, (self.padding, self.padding))

            # Background menu box for mass text (to the right)
            mass_x = kinematic_width + 2 * self.padding  # Place it after the kinematic text
            
            self.massRect =pygame.draw.rect(self.screen,self.colour, (mass_x, 0, mass_width + 2 * self.padding, height))
            self.screen.blit(mass_surface, (mass_x + self.padding, self.padding))
            
            # Background box for radius text (to the right)
            rad_x = kinematic_width + mass_width + 2 * self.padding  # Place it after the mass text
            self.radRect =pygame.draw.rect(self.screen, self.colour, (rad_x, 0, rad_width + 2 * self.padding, height))
            self.screen.blit(radius_surface, (rad_x + self.padding, self.padding))
         
            # Background box forlock text (to the right)
            lock_x = kinematic_width + mass_width + rad_width +  2 * self.padding  # Place it after the mass text
            self.lockRect =pygame.draw.rect(self.screen, lock_colour, (lock_x, 0, lock_width + 2 * self.padding, height))
            self.screen.blit(lock_surface, (lock_x + self.padding, self.padding))
            
            # Background box for view text (to the right)
            view_x = kinematic_width + mass_width + rad_width + lock_width +  2 * self.padding  # Place it after the mass text
            self.viewRect =pygame.draw.rect(self.screen, WHITE, (view_x, 0, view_width + 2 * self.padding, height))
            self.screen.blit(view_surface, (view_x + self.padding, self.padding))
            
