from .renderable import Renderable
from .direction import Direction
from .vector2d import Vector2D
import math
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
        # define the 3 points of the triangle that makes up the ship
        self.front = Vector2D(0, -SHIP_LENGTH / 2)
        self.aft_port = Vector2D(SHIP_WIDTH / 2, SHIP_LENGTH / 2)
        self.aft_starboard = Vector2D(-SHIP_WIDTH / 2, SHIP_LENGTH / 2)
        

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
    
    
    def rotate_point(self, point_x, point_y, center_x, center_y, angle_radians):
        # rotate the points
        x_rotated = (point_x * math.cos(angle_radians) - point_y * math.sin(angle_radians))
        y_rotated = (point_x * math.sin(angle_radians) + point_y * math.cos(angle_radians))

        # translate back
        return (x_rotated + center_x, y_rotated + center_y)
        #return (x_rotated, y_rotated)
    

    def get_polygon_points(self):
        # convert heading to radians for rotating
        angle_radians = math.radians(self.heading)

        a = self.rotate_point(self.front.x, self.front.y, self.pos.x, self.pos.y, angle_radians)
        b = self.rotate_point(self.aft_starboard.x, self.aft_starboard.y, self.pos.x, self.pos.y, angle_radians)
        c = self.rotate_point(self.aft_port.x, self.aft_port.y, self.pos.x, self.pos.y, angle_radians)
        
        return [a, b, c]


    def accelerate_ship(self, direction):
        acceleration = self.calculate_acceleration(ACCEL_RATE)

        match direction:
            case Direction.FORWARD:
                self.accel = acceleration
            case Direction.BACKWARD:
                acceleration.reverse()
                self.accel = acceleration
            case Direction.LEFT:
                pass
            case Direction.RIGHT:
                pass
            case Direction.CLOCKWISE:
                self.heading += MAX_ROTATIONAL_VELOCITY
            case Direction.ANTI_CLOCKWISE:
                self.heading -= MAX_ROTATIONAL_VELOCITY
                