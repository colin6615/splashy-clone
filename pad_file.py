"""holds the pad/trapoline class"""

import random

import arcade
import numpy as np

import my_constants
import player_file


class Pad(arcade.Sprite):
    """
    If player hits a pad, then the player bounces and the pad respawns below them.

    Class Attributes:
        Pad.list (SpriteList): list of all pad sprites

    Instance Attributes:
        center_x (float): horizontal position of a pad
        center_y (float): vertical position of a pad
    """

    def __init__(self, filename, sprite_scaling):
        """set default pad position"""
        super().__init__(filename, sprite_scaling)

        self.center_x = 0
        self.center_y = 0

    def spawn_pad(x_input, y_input):
        """
        spawns pads.

        Units are in terms of pads. If you drew a line from x=0 to x=2, then it has length of 2 * PAD_LENGTH.

        Args:
            x_input (float): the x-position of the center of the spawned pad.

            y_input (float): the y-position of the center of the spawned pad.
        """
        # make pad sprite
        pad = Pad("assets/green_rectangle.png", my_constants.SPRITE_SCALING_PAD)

        # position the pad
        pad.center_x = x_input * my_constants.PAD_LENGTH
        pad.center_y = y_input * my_constants.PAD_LENGTH

        Pad.list.append(pad)
        Pad.y_values_list = np.array([pad.center_y for pad in Pad.list])

    def setup():
        """Set up the game and initialize the variables."""
        Pad.list = None
        Pad.list = arcade.SpriteList()
        Pad.y_values_list = None
        Pad.y_values_list = []

        # spawn the first 2 pads
        for y in range(-2 * my_constants.DELTA_Y, 0, my_constants.DELTA_Y):
            Pad.spawn_pad(x_input=4, y_input=y)

    def update():
        # update the list of pad's y-positions.
        Pad.y_values_list = np.array([pad4.center_y for pad4 in Pad.list])

        # if the player moves below the pad, then kill player
        for pad3 in Pad.list:
            if pad3.center_y - player_file.Player.sprite.center_y > 5:
                gameview_file.GameView.dead = True

        # find pads that the player will hit
        hit_list = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Pad.list
        )
        # if the player hits a pad, then bounce player and move pad down.
        # there is probably a more efficient way of writing the next 2 loc.
        if len(hit_list) > 0:
            for hit_pad in hit_list:
                # move pad down
                hit_pad.center_y = (
                    min(Pad.y_values_list)
                    - my_constants.DELTA_Y * my_constants.PAD_LENGTH
                )
                # randomize pad's x-position
                hit_pad.center_x += random.randrange(
                    -my_constants.MOVE_PAD_X, my_constants.MOVE_PAD_X
                )

                # bounce player
                player_file.Player.sprite.velocity *= (
                    -my_constants.BOUNCE_DECAY_CONSTANT
                )

                # add to score
                gameview_file.GameView.score += 1 * gameview_file.GameView.score_factor
                gameview_file.GameView.time_factor += my_constants.TIME_FACTOR_CHANGE


import gameview_file
