from .vector2d import Vector2D
import pygame
from .game_constants import *

class AsteroidPart:
    def __init__(self, pos_x, pos_y, vel_x, vel_y, height, width, critical_part):
        pygame.init()
        self.pos = Vector2D(pos_x, pos_y)
        self.vel = Vector2D(vel_x, vel_y)
        self.width = width
        self.height = height

        self.rect = pygame.Rect(pos_x, pos_y, width, height)

        self.critical_part = critical_part
        if critical_part:
            self.colour = "purple"
        else:
            self.colour = "brown"

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

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y


    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect, 1)