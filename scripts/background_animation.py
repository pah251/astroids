from .vector2d import Vector2D
from .animation_constants import *
from .game_constants import *
import random

class BackgroundAnimation:
    def __init__(self):
        self.background_layers = []
        for i in range(BACKGROUND_ANIMATION_LAYERS):
            background_layer = []
            for j in range(BACKGROUND_NUMBER_OF_STARS):
                background_layer.append(Vector2D(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
            self.background_layers.append(background_layer)


    def update(self):
        # move the layer's objects by a fixed amount
        x_offset = BACKGROUND_ANIMATION_LAYER_SPEED_DELTA

        for animation_layer in self.background_layers:
            for background_object in animation_layer:
                background_object.x += x_offset
                
                # wrap objects that go off-screen
                if background_object.x >= SCREEN_WIDTH:
                    background_object.x = 0
                    # new random y-position to give illusion of brand new object
                    background_object.y = random.randint(0, SCREEN_HEIGHT)

            # increment the offset to move the next layer by a further amount
            # gives the illusion of speed
            x_offset += BACKGROUND_ANIMATION_LAYER_SPEED_DELTA
