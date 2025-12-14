import pygame
import random

from .vector2d import Vector2D
from .renderable import Renderable
from .asteroid_part import AsteroidPart
from .game_constants import *
from .asteroid_constants import *

class Asteroid(Renderable):
    def __init__(self, x_pos, y_pos, x_vel, y_vel):
        pygame.init()
        super().__init__()

        self.pos = Vector2D(x_pos, y_pos)
        self.vel = Vector2D(x_vel, y_vel)
        self.width = STARTING_WIDTH
        self.height = STARTING_HEIGHT

        self.asteroid_parts = []

    
    def build_asteroid(self, num_rectangles):
        for i in range (num_rectangles):
            x_offset = random.randint(0, STARTING_WIDTH) - STARTING_WIDTH / 2
            y_offset = random.randint(0, STARTING_HEIGHT) - STARTING_HEIGHT / 2

            width = random.randint(MIN_WIDTH, MAX_WIDTH)
            height = random.randint(MIN_HEIGHT, MAX_HEIGHT)

            new_asteroid_part = AsteroidPart(x_offset, y_offset, width, height, False)
            self.asteroid_parts.append(new_asteroid_part)
        

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