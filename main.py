#Notes
#1. Retrieving the scale factor every time really slows things down
# Prints are slowing performance
#Only draw things if they are on screen
#Bodies store their frame coordinate?


import pygame
import numpy as np
from menu import Menu
from body import Body
from scale import Scale
from bodymenu import BodyMenu
from clock import Clock
from camera import Camera
from pauser import Pauser
from constants import *

pygame.init()

clock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.RESIZABLE)
screen.fill((0, 0, 0))
pygame.display.set_caption("FALL - 2D Orbital Mechanics Simulator")

def handle_keypress(pressedKeys: dict) -> None:
    global running, paused, bodyMenu, typing, userInput, timePerFrame, camera, showMousePos
    if (pressedKeys[pygame.K_RETURN]):
        typing = False
        userInput = ""
        
    if (typing):
        userInput += event.unicode
        if (bodyMenu.massSelected):
            if (userInput.isdigit()):
                bodyMenu.body.set_mass(float(userInput))
            else:
                print("Invalid mass")
                typing = False
                userInput = ""
    
    if pressedKeys[pygame.K_f]:
        timePerFrame *=2
    if pressedKeys[pygame.K_ESCAPE]:
        running = False
    if pressedKeys[pygame.K_SPACE]:
        paused = not paused
    if pressedKeys[pygame.K_w] and bodyMenu.visible:
        bodyMenu.body.motionState[1][1] += 5
    if pressedKeys[pygame.K_s] and bodyMenu.visible:
        bodyMenu.body.motionState[1][1] -= 5
    if pressedKeys[pygame.K_d] and bodyMenu.visible:
        bodyMenu.body.motionState[1][0] += 5
    if pressedKeys[pygame.K_a] and bodyMenu.visible:
        bodyMenu.body.motionState[1][0] -= 5
    if pressedKeys[pygame.K_m] and bodyMenu.visible:
        bodyMenu.body.set_mass(bodyMenu.body.mass * 2)
    if pressedKeys[pygame.K_r] and bodyMenu.visible:
        bodyMenu.body.set_radius(bodyMenu.body.radius * 1.2)
        
    if pressedKeys[pygame.K_UP]:
        camera.y += 50*camera.scale  # Move the camera upwards
    if pressedKeys[pygame.K_DOWN]:
        camera.y -= 50*camera.scale  # Move the camera downwards
    if pressedKeys[pygame.K_LEFT]:
        camera.x -= 50*camera.scale  # Move the camera left
    if pressedKeys[pygame.K_RIGHT]:
        camera.x += 50*camera.scale  # Move the camera right
    if pressedKeys[pygame.K_LCTRL]:
        showMousePos = not showMousePos
        
    return

def handle_mousedown(event, menu):
    if event.button == 3:  # Right mouse button
        menu._menu_visible = True
        menu._menu_position = event.pos
        
    if event.button == 1: #left mouse button
        menu.button_click(event.pos[0], event.pos[1])
        menu._menu_visible = False

    global bodies, bodyMenu, typing
    if (bodyMenu.visible and bodyMenu.in_menu(event.pos)): #mouse click in the menu
        if (bodyMenu.in_mass_box(event.pos)):
            typing = True
            bodyMenu.massSelected = True
        else:
            bodyMenu.massSelected = False
        
        if (bodyMenu.in_lock_box(event.pos)):
            bodyMenu.body.locked = not bodyMenu.body.locked
        
        if (bodyMenu.in_view_box(event.pos)):
            bodyMenu.viewSelected = not bodyMenu.viewSelected
        return
    
    for body in bodies:
        if body.contains_frame_point(event.pos):
            #clicked a body
            bodyMenu.set_body(body)
            return
    bodyMenu.hide()

    global pauser, timePerFrame
    if pauser.in_forward_arrow(event.pos):
        timePerFrame *= 2
    if pauser.in_backward_arrow(event.pos):
        timePerFrame /= 2


def handle_mousewheel(event):
    global camera
    
    # Get the current mouse position on the screen (in frame coordinates)
    mousePos = pygame.mouse.get_pos()
    
    # Convert the mouse position to space coordinates
    mouseSpacePos = camera.space_coordinates(mousePos)
    
    # Adjust the scale factor based on scroll direction
    if event.y > 0:  # Scrolling up (zoom in)
        camera.set_scale_factor(camera.scale * 0.5)
    elif event.y < 0:  # Scrolling down (zoom out)
        camera.set_scale_factor(camera.scale * 2)
    
    # After scaling, convert the mouse position back to frame coordinates
    newMouseFramePos = camera.frame_coordinates(mouseSpacePos)
    
    # Calculate the difference between the mouse position and the new frame coordinates
    diff = (mousePos[0] - newMouseFramePos[0], mousePos[1] - newMouseFramePos[1])
    
    # Adjust the camera position in space coordinates
    camera.x -= diff[0] * camera.scale
    camera.y -= -diff[1] * camera.scale
    
 

def calculate_state(bodies):
    #calculate acceleration on each body
    for targetBody in bodies:
        netAcc = np.zeros((1,2)) #calculate acceleration on targetBody
        for actingBody in bodies:
            if (actingBody.id != targetBody.id):
                netAcc = netAcc + targetBody.acting_acceleration(actingBody)
        targetBody.motionState[2] = netAcc
    
    #adjust position, velocity accordingly
    global timePerFrame
    for body in bodies:
        if (not body.locked):
            dV = timePerFrame * body.motionState[2]
            body.motionState[1] = body.motionState[1] + dV
            dS = timePerFrame * body.motionState[1]
            #print(f"dS = {dS}")
            body.motionState[0] = body.motionState[0] + dS #change position
            

def show_mouse_pos():
    mousePos = camera.space_coordinates(pygame.mouse.get_pos())
    text = f"Pos: ({round(mousePos[0])}, {round(mousePos[1])})"
    mousePos = pygame.mouse.get_pos()

    # Render the text at the mouse position
    font = pygame.font.Font(None, 24)  # Default font with size 24
    text_surface = font.render(text, True, (255, 255, 255))  # White text
    text_width, text_height = text_surface.get_size()
    
    # Adjust text position to avoid overlapping with the mouse pointer
    text_x = mousePos[0] + 10  # Offset to the right of the cursor
    text_y = mousePos[1] - text_height - 10  # Offset slightly above the cursor
    
        # Draw a background rectangle behind the text for better visibility
    background_rect = pygame.Rect(text_x, text_y, text_width, text_height)
    pygame.draw.rect(screen, (0, 0, 0), background_rect)  # Black background
    screen.blit(text_surface, (text_x, text_y))
    



#Camera
camera = Camera();  

#bodies
bodies = pygame.sprite.Group()    

#Scale
scale = Scale(screen, camera)

# Right click menu
menu = Menu(screen, bodies, camera)

#Body Menu
bodyMenu = BodyMenu(screen)

#Pauser
pauser = Pauser(screen)


#Game time
timeSinceStart = 0
timePerFrame = 0.04
gameClock = Clock(screen)

#typing input
typing = False
userInput = ""

running = True
paused = False
showMousePos = False

frameNo = 0

while running:
    
    frameNo +=1

    #handle quit, click or keypress
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_keypress(pygame.key.get_pressed())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mousedown(event, menu)
        elif event.type == pygame.VIDEORESIZE:
            pass
        elif event.type == pygame.MOUSEWHEEL:
            handle_mousewheel(event)
    
    #update motion state of every body
    if (not paused):
        calculate_state(bodies)
        timeSinceStart += timePerFrame
    
    #set camera to position of body if viewing is selected
    if (bodyMenu.viewSelected):
        camera.set_camera_pos(bodyMenu.body.motionState[0])
    
    
    # Flip (update) the display only every 10th frame
    if frameNo%10 ==0:
        screen.fill((0, 0, 0))
        menu.flip()
        for body in bodies:
            body.draw_body()
        gameClock.update_clock(timeSinceStart)
        bodyMenu.update()
        scale.update()
        pauser.update()
        
        if (not paused): 
            gameClock.calculate_sim_speed(timePerFrame)
        
    if (showMousePos):
        show_mouse_pos()
        
    pygame.display.flip()
    
    clock.tick(1000)  # Run at normal speed when not paused
            