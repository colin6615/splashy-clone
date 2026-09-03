import random

import arcade


def spawn(x_input, y_input, image_path, image_scale, Input_class):
    """
    spawns an item at specified coordinates

    Args:
        x_input (float): the x-position of the center of the spawned item.

        y_input (float): the y-position of the center of the spawned item.
    """
    # make item sprite
    item = Input_class(
        image_path, image_scale
    )  # need some way to get self.image_path without calling self?

    # position the pad
    item.center_x = x_input
    item.center_y = y_input

    Input_class.list.append(item)


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
