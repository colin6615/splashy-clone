import random

import arcade


class Item(arcade.Sprite):
    # make it so the random numbers generated in this class are the same in every run of the game.
    # remove upon release
    random.seed(10)

    def _update(self, delta_time):  # **kwargs
        # children will overide this to inserrt their specific code
        pass

    def update(self, delta_time):  # **kwargs
        # Run general item stuff

        # Call the child's specific logic
        self._update(delta_time)  # **kwargs

