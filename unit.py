
from point import *

class Unit(Point):
    def __init__(self, x, y, rad, speed, red, green, blue, radius):
        Point.__init__(self, x, y)
        self.rad = rad
        self.speed = speed
        self.red = red
        self.green = green
        self.blue = blue
        self.radius = radius