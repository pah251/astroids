from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    ASTEROIDS_GAME = auto()
    ASTEROIDS_GAME_OVER = auto()