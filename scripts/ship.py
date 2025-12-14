from .renderable import Renderable
from .direction import Direction
from .vector2d import Vector2D
import math
from .ship_constants import *
from .game_constants import *

class Ship(Renderable):
    def __init__(self, start_x, start_y):
        super().__init__()
        
        # inital vectors for the ship
        self.vel = Vector2D(0,0)
        self.accel = Vector2D(0,0)
        self.rot_vel = 0

        # x,y coordinates on the map
        self.pos = Vector2D(start_x, start_y)
        # direction, 0 to 360 degrees
        self.heading = 0
        # define the 3 points of the triangle that makes up the ship
        self.front = Vector2D(0, -SHIP_LENGTH / 2)
        self.aft_port = Vector2D(SHIP_WIDTH / 2, SHIP_LENGTH / 2)
        self.aft_starboard = Vector2D(-SHIP_WIDTH / 2, SHIP_LENGTH / 2)

        # define the imaginary radius for crude collision detection
        self.radius = SHIP_LENGTH / 2
        

    def update(self):
        self.pos.add_vector2d(self.vel)
        self.heading += self.rot_vel

        if self.pos.x >= SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.y >= SCREEN_HEIGHT:
            self.pos.y = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        if self.pos.y < 0:
            self.pos.y = SCREEN_HEIGHT
            

    def calculate_acceleration(self):
        angle_radians = math.radians(90 - self.heading)

        accel_x = ACCEL_RATE * math.cos(angle_radians)
        accel_y = ACCEL_RATE * math.sin(angle_radians)

        return Vector2D(accel_x, -accel_y)
    

    def get_front_point(self):
        angle_radians = math.radians(self.heading)
        front_point = self.rotate_point(self.front.x, self.front.y, self.pos.x, self.pos.y, angle_radians)
        return Vector2D(front_point[0], front_point[1])
    
    
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
        acceleration = self.calculate_acceleration()

        match direction:
            case Direction.FORWARD:
                self.vel.add_vector2d(acceleration)
            case Direction.BACKWARD:
                self.vel.subtract_vector2d(acceleration)
            case Direction.LEFT:
                pass
            case Direction.RIGHT:
                pass
            case Direction.CLOCKWISE:
                self.rot_vel += ROTATIONAL_ACCEL_RATE
            case Direction.ANTI_CLOCKWISE:
                self.rot_vel -= ROTATIONAL_ACCEL_RATE


    def check_collision(self, asteroids):
        ship_points = self.get_polygon_points()
        for asteroid in asteroids:
            for asteroid_part in asteroid.asteroid_parts:
                for x, y in ship_points:
                    if asteroid_part.rect.collidepoint(x, y):
                        return True
        
