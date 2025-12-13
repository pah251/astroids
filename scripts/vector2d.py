import math

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_vector2d(self, vector):
        self.x += vector.x
        self.y += vector.y

    def subtract_vector2d(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def magnitude(self):
        return math.sqrt((self.x  * self.x) + (self.y * self.y))