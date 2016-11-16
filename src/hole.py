
from point import *

class Hole(Point):
    def __init__(self, x, y, r):
        Point.__init__(self, x, y)
        self.radius = r
