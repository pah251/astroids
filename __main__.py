from .scripts.game import Game
from .scripts.game_constants import *

if __name__ == "__main__":
    game = Game((SCREEN_WIDTH,SCREEN_HEIGHT), BACKGROUND_COLOUR)
    game.game_init()
    game.game_loop()