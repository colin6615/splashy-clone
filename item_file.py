import random

import arcade


def spawn(x_input, y_input, **input_dict):
    """
    spawns an item at specified coordinates. Adds item to sprite list.

    Args:
        x_input (float): the x-position of the center of the spawned item.
        y_input (float): the y-position of the center of the spawned item.

    Kwargs from **input_dict:
        Input_class (class): the sprite's class.
        image_path (string): file directory of sprite image
        image_scale (float): changes size of sprite
    """
    # Make dummy variables to improve code readability. This is probably bad practice. rewrite, this, later, if needed.
    class_ = input_dict["Input_class"]
    image_path_ = input_dict["image_path"]
    scale_ = input_dict["image_scale"]
    # make sprite
    item = class_(image_path_, scale_)

    # position the sprite
    item.center_x = x_input
    item.center_y = y_input

    # add item to sprite list
    class_.list.append(item)


class Item(arcade.Sprite):
    # make it so the random numbers generated in this class are the same in every run of the game.
    # remove upon release
    random.seed(10)

    def _update(self, delta_time):  # **kwargs
        """Child update Code
        children will overide this to inserrt their specific code"""

    def update(self, delta_time):  # **kwargs
        """Parent's update code
        Every child will run this general update code"""
        # Run general item stuff

        # Call the child's specific logic
        self._update(delta_time)  # **kwargs
