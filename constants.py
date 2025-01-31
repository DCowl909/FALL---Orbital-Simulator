#Numerical Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750
DEFAULT_RADIUS = 100
DEFAULT_MASS = 1000
DEFAULT_SCALE_FACTOR = 10
G = 6.67430 * pow(10, -1)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
SOFT_RED = (150, 0, 0)
SOFT_GREEN = (0, 150, 0 )
SPACE_BLUE = (52, 55, 235)
PINK = (252, 162, 178)


#Pause button
TRIANGLE_SIZE = 35
PAUSE_WIDTH = 5
PAUSE_HEIGHT = 15

def is_on_screen(framePos):
    return 0 <= framePos[0] < SCREEN_WIDTH and 0 <= framePos[1] < SCREEN_HEIGHT