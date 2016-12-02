
from point import *

class Ball(Point):
    id = 0
    def __init__(self, x, y, rad, speed, red, green, blue, radius):
        Point.__init__(self, x, y)
        self.rad = rad
        self.speed = speed
        self.red = red
        self.green = green
        self.blue = blue
        self.radius = radius
        self.enable = True
        self.id = Ball.id
        Ball.id += 1
    
    @staticmethod
    def id_reset():
        Ball.id = 0