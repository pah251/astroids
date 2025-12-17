import pygame
#from scripts.astroid import Asteroid
from .ship import Ship
from .direction import Direction
from .game_state import GameState
from .projectile_controller import ProjectileController
from .asteroid_controller import AsteroidController
from .background_animation import BackgroundAnimation
from .projectile_constants import *
from .animation_constants import *
from .game_constants import *

class Game:
    def __init__(self, screen_size, screen_colour):
        self.screen_size = screen_size
        self.screen_colour = screen_colour
        self.game_state = GameState.MAIN_MENU
        self.hi_score = 0
        self.score = 0
        self.background_animation = BackgroundAnimation()

    def pygame_init(self):
        pygame.init()
        self.font = pygame.font.Font(None, size=40)
        self.screen = pygame.display.set_mode(self.screen_size)


    def game_init(self):
        # create player entity
        self.player = Ship(STARTING_X_POS, STARTING_Y_POS)

        # controllers for game entities
        self.asteroid_controller = AsteroidController()
        self.projectile_controller = ProjectileController()

        # spawn asteroids
        for i in range (STARTING_ASTEROIDS):
            self.asteroid_controller.spawn_asteroid()

        # select appropriate game state
        self.game_state = GameState.ASTEROIDS_GAME
        
        # counter for score
        self.score = 0


    def main_menu(self):
        self.screen.fill(self.screen_colour)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.game_init()
            return GameState.ASTEROIDS_GAME
        
        game_over_text = self.font.render('ASTROIDS', True, (255,255,255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 25))        
        continue_text = self.font.render('Press space to play!', True, (255, 255, 255))
        self.screen.blit(continue_text, (SCREEN_WIDTH/2 - 175, SCREEN_HEIGHT/2 + 25))

        pygame.display.flip()

        return GameState.MAIN_MENU


    def game_over(self):
        self.screen.fill(self.screen_colour)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.game_init()
            return GameState.ASTEROIDS_GAME
        
        game_over_text = self.font.render('GAME OVER', True, (255,255,255))
        continue_text = self.font.render('Press space to play again...', True, (255, 255, 255))

        if self.score > self.hi_score:
            score_text = self.font.render(f"NEW HIGH SCORE: {self.score}", True, (255,255,255))    
            self.hi_score = self.score
        else:
            score_text = self.font.render(f"SCORE: {self.score}", True, (255,255,255))
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 25))
        self.screen.blit(score_text, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 25))
        self.screen.blit(continue_text, (SCREEN_WIDTH/2 - 175, SCREEN_HEIGHT/2 + 125))
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
        self.asteroid_controller.update(dt)                    
        self.projectile_controller.update(dt)
        self.background_animation.update()

        # check for collisions between player and astroids
        # end the game if so
        game_over = self.player.check_collision(self.asteroid_controller.asteroids)
        if game_over == True:
            return GameState.ASTEROIDS_GAME_OVER
        
        # check for collisions between projectiles and asteroids
        # increment score if destroyed asteroid core
        self.score += self.asteroid_controller.check_collisions(self.projectile_controller.projectiles)
        
        # handle rendering
        self.screen.fill(self.screen_colour)

        # draw the background
        self.background_animation.draw(self.screen)
        
        # draw the player's ship
        self.player.draw(self.screen)

        # draw the asteroids
        self.asteroid_controller.draw(self.screen)
        # draw projectiles
        self.projectile_controller.draw(self.screen)
            

        # draw counter for score
        score_text = self.font.render(f"SCORE: {self.score}", True, (255,255,255))
        self.screen.blit(score_text, (10, 10))

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

            if self.game_state == GameState.MAIN_MENU:
                self.game_state = self.main_menu()
            elif self.game_state == GameState.ASTEROIDS_GAME:
                self.game_state = self.asteroids_game(dt)
            elif self.game_state == GameState.ASTEROIDS_GAME_OVER:
                self.game_state = self.game_over()
            
        self.game_quit()
    
    def game_quit(self):
        pygame.quit()
        quit()