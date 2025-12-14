import pygame
#from scripts.astroid import Asteroid
from .ship import Ship
from .direction import Direction
from .asteroid import Asteroid
from .projectile_controller import ProjectileController
from .projectile_constants import *
from .game_constants import *

class Game:
    def __init__(self, screen_size, screen_colour):
        self.screen_size = screen_size
        self.screen_colour = screen_colour
        self.player = Ship(STARTING_X_POS, STARTING_Y_POS)
        self.asteroids = [Asteroid(500, 500, -0.5, -0.5), Asteroid(500, 100, 1, 0.25)]
        self.projectile_controller = ProjectileController()
        # list of object to render
        self.render_items = [self.player]
        self.render_items.append(self.asteroids)

    def game_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)


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

            for asteroid in self.asteroids:
                asteroid.update()
            
            self.projectile_controller.update_projectiles(dt)

            
            # handle rendering
            self.screen.fill(self.screen_colour)
            
            pygame.draw.polygon(self.screen, "white", self.player.get_polygon_points())
            pygame.draw.circle(self.screen, "green", (self.player.pos.x, self.player.pos.y), 2)

            for asteroid in self.asteroids:
                rect = pygame.Rect(asteroid.pos.x, asteroid.pos.y, 75, 75)
                pygame.draw.rect(self.screen, "brown", rect)

            for projectile in self.projectile_controller.projectiles:
                pygame.draw.circle(self.screen, PROJECTILE_COLOUR, (projectile.pos.x, projectile.pos.y), PROJECTILE_RADIUS)

            # update display
            pygame.display.flip()

        self.game_end()
    
    def game_end(self):
        pygame.quit()

    