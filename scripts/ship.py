from .renderable import Renderable
from .direction import Direction
from .vector2d import Vector2D

from .ship_constants import *
from .game_constants import *

class Ship(Renderable):
    # inital vectors for the ship
    vel = Vector2D(0,0)
    accel = Vector2D(0,0)
    rot_vel = 0
    rot_accel = 0

    def __init__(self, start_x, start_y):
        super().__init__()

        # x,y coordinates on the map
        self.pos = Vector2D(start_x, start_y)
        # direction, 0 to 360 degrees
        self.heading = 0
        

    def update(self):
        self.vel.add_vector2d(self.accel)
        self.pos.add_vector2d(self.vel)

        # reset acceleration now we've applied it to velocity
        self.accel.x = 0
        self.accel.y = 0

        if self.pos.x >= SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.y >= SCREEN_HEIGHT:
            self.pos.y = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        if self.pos.y < 0:
            self.pos.y = SCREEN_HEIGHT

    def calculate_acceleration(self, delta_a):
        return Vector2D(0, ACCEL_RATE)
    

    def get_polygon_points(self):
        front = (self.pos.x, self.pos.y + SHIP_LENGTH / 2)
        aft_port = (self.pos.x - (SHIP_WIDTH / 2), self.pos.y - (SHIP_LENGTH / 2))
        aft_starboard = (self.pos.x + (SHIP_WIDTH / 2), self.pos.y - (SHIP_LENGTH /2))
        
        return [front, aft_port, aft_starboard]


    def accelerate_ship(self, direction):
        acceleration = self.calculate_acceleration(ACCEL_RATE)

        match direction:
            case Direction.FORWARD:
                self.accel = acceleration
            case Direction.BACKWARD:
                acceleration.reverse()
                self.accel = acceleration
                