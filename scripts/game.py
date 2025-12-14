import pygame
#from scripts.astroid import Asteroid
from .ship import Ship
from .direction import Direction
from .game_state import GameState
from .projectile_controller import ProjectileController
from .asteroid_controller import AsteroidController
from .projectile_constants import *
from .game_constants import *

class Game:
    def __init__(self, screen_size, screen_colour):
        self.screen_size = screen_size
        self.screen_colour = screen_colour


    def pygame_init(self):
        pygame.init()
        self.font = pygame.font.Font(None, size=40)


    def game_init(self):
        self.player = Ship(STARTING_X_POS, STARTING_Y_POS)
        self.asteroid_controller = AsteroidController()
        self.projectile_controller = ProjectileController()
        self.player.pos.x = STARTING_X_POS
        self.player.pos.y = STARTING_Y_POS
        self.screen = pygame.display.set_mode(self.screen_size)
        self.asteroid_controller.spawn_asteroid()
        self.asteroid_controller.spawn_asteroid()
        self.asteroid_controller.spawn_asteroid()
        self.game_state = GameState.ASTEROIDS_GAME



    def main_menu(self):
        pass


    def game_over(self):
        self.screen.fill(self.screen_colour)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.game_init()
            return GameState.ASTEROIDS_GAME
        
        game_over_text = self.font.render('GAME OVER', True, (255,255,255))
        continue_text = self.font.render('Press space to play again...', True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 25))
        self.screen.blit(continue_text, (SCREEN_WIDTH/2 - 175, SCREEN_HEIGHT/2 + 25))
        pygame.display.flip()
        return GameState.ASTEROIDS_GAME_OVER
        


    def asteroids_game(self, dt):        
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

        game_over = self.player.check_collision(self.asteroid_controller.asteroids)
        if game_over == True:
            return GameState.ASTEROIDS_GAME_OVER
        self.asteroid_controller.check_collisions(self.projectile_controller.projectiles)
        
        # handle rendering
        self.screen.fill(self.screen_colour)
        
        # draw the player's ship
        pygame.draw.polygon(self.screen, "white", self.player.get_polygon_points())
        ship_front = self.player.get_front_point()
        pygame.draw.circle(self.screen, "green", (ship_front.x, ship_front.y), 1)

        # draw the asteroids
        for asteroid in self.asteroid_controller.asteroids:
            for asteroid_part in asteroid.asteroid_parts:
                pygame.draw.rect(self.screen, asteroid_part.colour, asteroid_part.rect)

        for projectile in self.projectile_controller.projectiles:
            pygame.draw.rect(self.screen, PROJECTILE_COLOUR, projectile.rect)

        # update display
        pygame.display.flip()

        return GameState.ASTEROIDS_GAME


    def game_loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_quit()

            if self.game_state == GameState.ASTEROIDS_GAME:
                self.game_state = self.asteroids_game(dt)
            elif self.game_state == GameState.ASTEROIDS_GAME_OVER:
                self.game_state = self.game_over()
            

        self.game_quit()
    
    def game_quit(self):
        pygame.quit()
        quit()

    