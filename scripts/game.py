import pygame
#from scripts.astroid import Asteroid
from .ship import Ship
from .direction import Direction

class Game:
    def __init__(self, screen_size, screen_colour):
        self.screen_size = screen_size
        self.screen_colour = screen_colour
        self.player = Ship(50, 50)
        # list of object to render
        self.render_items = [self.player]

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

            # render
            self.screen.fill(self.screen_colour)
            player_rect = self.rectangle = pygame.Rect(self.player.pos.x, self.player.pos.y, 50, 100)
            pygame.draw.rect(self.screen, "white", player_rect)

            # update display
            pygame.display.flip()

        self.game_end()
    
    def game_end(self):
        pygame.quit()

    