from .asteroid import Asteroid
from .game_constants import *
from .asteroid_constants import *
import random

class AsteroidController:
    def __init__(self):
        self.asteroids = []


    def spawn_asteroid(self):
        asteroid_spawn_pos_x = 0
        asteroid_spawn_pos_y = 0

        # asteroids spawn on screen border, random 1-4 to choose a side of the screen
                
        spawn_side = random.randint(1,4)
        if spawn_side == 1: # top
            asteroid_spawn_pos_x = random.randint(0, SCREEN_WIDTH)
        if spawn_side == 2: # right
            asteroid_spawn_pos_x = SCREEN_WIDTH
            asteroid_spawn_pos_y = random.randint(0, SCREEN_HEIGHT)
        if spawn_side == 3: # bottom
            asteroid_spawn_pos_x = random.randint(0, SCREEN_WIDTH)
            asteroid_spawn_pos_y = SCREEN_HEIGHT
        if spawn_side == 4: # left
            asteroid_spawn_pos_y = random.randint(0, SCREEN_HEIGHT)
        
        asteroid_spawn_vel_x = random.randrange(-MAX_X_VELOCITY, MAX_X_VELOCITY)
        asteroid_spawn_vel_y = random.randrange(-MAX_Y_VELOCITY, MAX_Y_VELOCITY)

        num_asteroid_parts = random.randint(1, MAX_ASTEROID_PARTS)

        new_asteroid = Asteroid(
            asteroid_spawn_pos_x, asteroid_spawn_pos_y,
            asteroid_spawn_vel_x, asteroid_spawn_vel_y,
        )
        
        new_asteroid.build_asteroid(num_asteroid_parts)
        
        self.asteroids.append(new_asteroid)


    def update_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.update()


    def check_collisions(self, projectiles):
        num_collisions = 0
        for asteroid in self.asteroids:
            destroy = asteroid.check_collision(projectiles)
            if destroy == True:
                self.asteroids.remove(asteroid)
                
                # increment the number of collisions for the score
                num_collisions += 1

        return num_collisions
