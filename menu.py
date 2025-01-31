from body import Body
import pygame
import numpy as np
from constants import *

#Right click menu
class Menu():
    menu_items = ["Create Body", "Option 2", "Option 3"]
    menu_width, menu_height = 150, 30 * len(menu_items)
    
    def __init__(self, screen, bodyGroup, camera):
        self.group = bodyGroup
        self._screen = screen
        self.camera = camera #could be initalised here?
        self._menu_visible = False
        self._menu_position = (0, 0)
        self._menu_actions = {
        0: self.option_1,
        1: self.option_2,
        2: self.option_3
        }

        
    def flip(self):
        if self._menu_visible:
            menu_x, menu_y = self._menu_position
            pygame.draw.rect(self._screen, GRAY, (menu_x, menu_y, Menu.menu_width, Menu.menu_height))
            for i, item in enumerate(Menu.menu_items):
                item_rect = pygame.Rect(menu_x, menu_y + i * 30, Menu.menu_width, 30)
                pygame.draw.rect(self._screen, WHITE, item_rect, 1)  # Draw item border
                text = pygame.font.Font(None, 24).render(item, True, BLUE)
                self._screen.blit(text, (menu_x + 10, menu_y + i * 30 + 5))
            
                
    def button_click(self, mouse_x, mouse_y):
        if self._menu_visible:
            menu_x, menu_y = self._menu_position
            if menu_x <= mouse_x <= menu_x + Menu.menu_width and menu_y <= mouse_y <= menu_y + Menu.menu_height:
                clicked_item = (mouse_y - menu_y) // 30
                if clicked_item in self._menu_actions:
                    self._menu_actions[clicked_item]()  # Call the associated function
                    menu_visible = False  # Close the menu after selection
                else:
                    menu_visible = False  # Close the menu if clicked outside
                
    def option_1(self):
        motionState = np.zeros((3,2))
        motionState[0] = self.camera.space_coordinates(self._menu_position)
        newBody = Body(motionState, self.group, self._screen, self.camera)
        self.group.add(newBody)
        print("SPAWN")
        pass
    
    def option_2(self):
        print("SPAWN 2")
        pass
    
    def option_3(self):
        print("SPAWN 3")
        pass
