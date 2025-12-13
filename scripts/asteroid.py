from .vector2d import Vector2D
from .renderable import Renderable
from .game_constants import *

class Asteroid(Renderable):
    def __init__(self, x_pos, y_pos, x_vel, y_vel):
        super().__init__()

        self.pos = Vector2D(x_pos, y_pos)
        self.vel = Vector2D(x_vel, y_vel)

    def update(self):
        self.pos.add_vector2d(self.vel)
        if self.pos.x >= SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.y >= SCREEN_HEIGHT:
            self.pos.y = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        if self.pos.y < 0:
            self.pos.y = SCREEN_HEIGHT
    