from constants import SCREEN_HEIGHT, SCREEN_WIDTH, DEFAULT_SCALE_FACTOR

class Camera():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.scale = DEFAULT_SCALE_FACTOR
    
    def space_coordinates(self, frameCoordinate):
        x = (frameCoordinate[0] - SCREEN_WIDTH/2) * self.scale + self.x
        y = (SCREEN_HEIGHT/2 - frameCoordinate[1]) * self.scale + self.y
        
        return (x, y)
    
    def frame_coordinates(self, spaceCoordinates):
        x = (spaceCoordinates[0] - self.x) / self.scale + SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 - (spaceCoordinates[1] - self.y) / self.scale
    
        return (x, y)
    
    def set_scale_factor(self, scaleFactor):
        self.scale = scaleFactor
        
    def set_camera_pos(self, cameraPos):
        self.x = cameraPos[0]
        self.y = cameraPos[1]

