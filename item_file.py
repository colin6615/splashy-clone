import random

import arcade


class Item(arcade.Sprite):
    # make it so the random numbers generated in this class are the same in every run of the game.
    # remove upon release
    random.seed(10)

    def __init__(self, filename, sprite_scaling):
        """set default pad position"""
        super().__init__(filename, sprite_scaling)

        self.center_x = 0
        self.center_y = 0

    def _update(self, delta_time):  # **kwargs
        # children will overide this to inserrt their specific code
        pass

    def update(self, delta_time):  # **kwargs
        # Run general item stuff

        # Call the child's specific logic
        self._update(delta_time)  # **kwargs

    def spawn(x_input, y_input, image_path, image_scaler, item_class):
        """
        spawns pads.

        Units are in terms of pads. If you drew a line from x=0 to x=2, then it has length of 2 * PAD_LENGTH.

        Args:
            x_input (float): the x-position of the center of the spawned pad.

            y_input (float): the y-position of the center of the spawned pad.
        """
        # make pad sprite
        item = Item(image_path, image_scaler)

        # position the pad
        item.center_x = x_input
        item.center_y = y_input

        item_class.list.append(item)
