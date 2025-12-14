from .vector2d import Vector2D

class AsteroidPart:
    def __init__(self, pos_x, pos_y, height, width, critical_part):
        self.core_offset = Vector2D(pos_x, pos_y)
        self.height = height
        self.width = width
        self.critical_part = critical_part