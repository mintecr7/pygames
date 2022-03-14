import pygame

WIDTH, HEIGHT = 700, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Paddle:
    COLOR = WHITE
    VELOCITY = 5
    def __init__(self, x, y, height, width) -> None:
        self.x = self.orginal_x = x
        self.y = self.orginal_y = y
        self.height = height
        self.width = width
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
        pygame.display.update()
    
    def move(self, up=True):
        if up and self.y-self.VELOCITY>=0:
            self.y -= self.VELOCITY
        elif not up and self.y + self.height + self.VELOCITY <= HEIGHT:
            self.y += self.VELOCITY  
    def rest(self):
        self.x = self.orginal_x
        self.y = self.orginal_y 
         
class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    def __init__(self, x, y, radius) -> None:
        self.x = self.orginal_x = x
        self.y = self.orginal_y = y
        self.radius = radius
        self.x_val = self.MAX_VEL
        self.y_val = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    def move(self):
        self.x += self.x_val
        self.y += self.y_val
    def rest(self):
        self.x = self.orginal_x
        self.y = self.orginal_y
        self.x_val *= -1 
        self.y_val = 0
         