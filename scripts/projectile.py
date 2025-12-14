from .renderable import Renderable
from .vector2d import Vector2D
from .projectile_constants import *
from .game_constants import *
import math

class Projectile(Renderable):
    def __init__(self, x_pos, y_pos, heading):
        super().__init__()

        self.pos = Vector2D(x_pos, y_pos)
        self.heading = heading
        self.vel = self.calculate_velocity(heading)
        

    def calculate_velocity(self, heading):
        angle_radians = math.radians(90 - heading)
        
        x_vel = PROJECTILE_VELOCITY * math.cos(angle_radians)
        y_vel = PROJECTILE_VELOCITY * math.sin(angle_radians)

        # invert the y value because of pygame being pygame
        return Vector2D(x_vel, -y_vel)


    def update(self):
        self.pos.add_vector2d(self.vel)

        # check for going off the screen -> if so return false so the game controller knows to stop drawing it
        if self.pos.x < 0 or self.pos.x > SCREEN_WIDTH or self.pos.y < 0 or self.pos.y > SCREEN_HEIGHT:
            return False
        return True