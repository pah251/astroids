from .scripts.game import Game

if __name__ == "__main__":
    game = Game((640,640), "black")
    game.game_init()
    game.game_loop()