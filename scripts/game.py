import pygame
#from scripts.astroid import Asteroid
from .ship import Ship
from .direction import Direction
from .asteroid import Asteroid

class Game:
    def __init__(self, screen_size, screen_colour):
        self.screen_size = screen_size
        self.screen_colour = screen_colour
        self.player = Ship(50, 50)
        self.asteroids = [Asteroid(500, 500, -0.5, -0.5), Asteroid(500, 100, 1, 0.25)]
        # list of object to render
        self.render_items = [self.player]
        self.render_items.append(self.asteroids)

    def game_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)


    def game_loop(self):
        clock = pygame.time.Clock()
        fps = 60
        running = True
        while running:
            dt = clock.tick(fps)
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            # updates
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.player.accelerate_ship(Direction.FORWARD)
            if keys[pygame.K_DOWN]:
                self.player.accelerate_ship(Direction.BACKWARD)

            self.player.update()
            for asteroid in self.asteroids:
                asteroid.update()

            # render
            self.screen.fill(self.screen_colour)
            
            pygame.draw.polygon(self.screen, "white", self.player.get_polygon_points())

            for asteroid in self.asteroids:
                rect = pygame.Rect(asteroid.pos.x, asteroid.pos.y, 75, 75)
                pygame.draw.rect(self.screen, "brown", rect)

            # update display
            pygame.display.flip()

        self.game_end()
    
    def game_end(self):
        pygame.quit()

    