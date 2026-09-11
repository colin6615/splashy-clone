"""Defines the Item class and spawn() function

Item is a parent class of Pad, Coin, Target, and Spike. The class doesn't do anything on its own.

I refer to Item's children as "items." These items are sprites that the player can interact with

The spawn() function creates a sprite and adds it to a sprite list.
"""

import random

import arcade


class Item(arcade.Sprite):
    """
    Instance Attributes:
        center_x (float): horizontal position of a pad
        center_y (float): vertical position of a pad
    """

    # make it so the random numbers generated in this class are the same in every run of the game.
    # upon release: remove.
    random.seed(10)

    def __init__(self, filename, sprite_scaling):
        """set default pad position"""
        super().__init__(filename, sprite_scaling)

        self.center_x = 0
        self.center_y = 0


def spawn(x_input, y_input, **input_dict):
    """
    spawns an item at specified coordinates

    Args:
        x_input (float): the x-position of the center of the spawned item.
        y_input (float): the y-position of the center of the spawned item.

    Kwargs from **input_dict:
        Input_class (class): the sprite's class.
        image_path (string): file directory of sprite image
        image_scale (float): changes size of sprite

    returns:
        the spawned item
    """
    # Make dummy variables to improve code readability. This is probably bad practice. rewrite, this, later, if needed.
    image_path = input_dict["image_path"]
    image_scale = input_dict["image_scale"]

    # the Input_class key is defined at the bottom of coin_file, pad_file, target_file, and spike_file
    class_ = input_dict["Input_class"]

    # make sprite. load texture.
    # this works because class_ is a grandchild of the Sprite class.
    item = class_(image_path, image_scale)

    # position the sprite
    item.center_x = x_input
    item.center_y = y_input

    return item
