import arcade
import numpy as np

import my_constants


class Pad(arcade.SpriteList):
    def spawn_pad(x_input, y_input):
        """
        spawns a 3x1 structure of pads.
        Args:
            x (int): the x-position of the center of one of the pads (I'm not sure which pad it is). Units are in terms of pads. If you drew a line from x=0 to x=2, then it has length of 2 * PAD_LENGTH. I don't know what the PAD_LENGTH is.

            y (int): the y-position of the center of all of the pads. Units are in terms of pads.

        """
        pad = arcade.Sprite(
            "assets/green_rectangle.png", my_constants.SPRITE_SCALING_PAD
        )
        # position the pad
        pad.center_x = x_input * my_constants.PAD_LENGTH
        pad.center_y = y_input * my_constants.PAD_LENGTH
        Pad.list.append(pad)
        Pad.y_values_list = np.array([pad.center_y for pad in Pad.list])

    def update(self, delta_time):
        if pad.center_y != 0:
            print("hi")
        # - player_sprite.center_y > 5:
