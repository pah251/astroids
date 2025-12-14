import pygame
#from scripts.astroid import Asteroid
from .ship import Ship
from .direction import Direction
from .asteroid import Asteroid
from .projectile_controller import ProjectileController
from .asteroid_controller import AsteroidController
from .projectile_constants import *
from .game_constants import *

class Game:
    def __init__(self, screen_size, screen_colour):
        self.screen_size = screen_size
        self.screen_colour = screen_colour
        self.player = Ship(STARTING_X_POS, STARTING_Y_POS)
        self.asteroid_controller = AsteroidController()
        self.projectile_controller = ProjectileController()
        # list of object to render
        self.render_items = [self.player]


    def game_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.asteroid_controller.spawn_asteroid()
        self.asteroid_controller.spawn_asteroid()
        self.asteroid_controller.spawn_asteroid()


    def game_loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(FPS)
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # handle player input
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.player.accelerate_ship(Direction.FORWARD)
            if keys[pygame.K_s]:
                self.player.accelerate_ship(Direction.BACKWARD)
            if keys[pygame.K_q]:
                self.player.accelerate_ship(Direction.LEFT)
            if keys[pygame.K_e]:
                self.player.accelerate_ship(Direction.RIGHT)
            if keys[pygame.K_d]:
                self.player.accelerate_ship(Direction.CLOCKWISE)
            if keys[pygame.K_a]:
                self.player.accelerate_ship(Direction.ANTI_CLOCKWISE)
            if keys[pygame.K_SPACE]:
                spawn_point = self.player.get_front_point()
                self.projectile_controller.spawn_projectile(spawn_point.x, spawn_point.y, self.player.heading)

            # update the game state
            self.player.update()

            self.asteroid_controller.update_asteroids()
                        
            self.projectile_controller.update_projectiles(dt)

            
            # handle rendering
            self.screen.fill(self.screen_colour)
            
            # draw the player's ship
            pygame.draw.polygon(self.screen, "white", self.player.get_polygon_points())
            pygame.draw.circle(self.screen, "green", (self.player.pos.x, self.player.pos.y), 2)

            # draw the asteroids
            for asteroid in self.asteroid_controller.asteroids:
                for asteroid_part in asteroid.asteroid_parts:
                    pygame.draw.rect(self.screen, asteroid_part.colour, asteroid_part.rect)

            for projectile in self.projectile_controller.projectiles:
                pygame.draw.rect(self.screen, PROJECTILE_COLOUR, projectile.rect)

            # update display
            pygame.display.flip()

        self.game_end()
    
    def game_end(self):
        pygame.quit()

    