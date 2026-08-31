"""Module summary phrase. Detailed description of what this module does, what classes/functions it exposes, and any usage examples if applicable.

Short one-line summary of the class's purpose.

A longer description explaining what the class does, its general state, and how it is meant to be used across your program.
Attributes:
input_path (str): Description of the attribute
"""

import random

import arcade
import numpy as np

import gameview_file
import my_constants


class Pad(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        """Constructor."""
        # Call the parent class (Sprite) constructor
        super().__init__(filename, sprite_scaling)

        # set position
        self.center_x = 0
        self.center_y = 0

    def spawn_pad(self, x_input, y_input):
        """
        spawns a 3x1 structure of pads.
        Args:
            x (int): the x-position of the center of one of the pads (I'm not sure which pad it is). Units are in terms of pads. If you drew a line from x=0 to x=2, then it has length of 2 * PAD_LENGTH. I don't know what the PAD_LENGTH is.

            y (int): the y-position of the center of all of the pads. Units are in terms of pads.

        Returns:
            Return (type): What is returned and why.

        """
        pad = Pad("assets/green_rectangle.png", my_constants.SPRITE_SCALING_PAD)
        # position the pad
        pad.center_x = x_input * my_constants.PAD_LENGTH
        pad.center_y = y_input * my_constants.PAD_LENGTH
        Pad.list.append(pad)

    def setup():
        """Set up the game and initialize the variables."""
        # lists
        Pad.list = None
        Pad.list = arcade.SpriteList()
        Pad.y_values_list = None
        Pad.y_values_list = []

        # spawn the first 2 pads
        for y in range(-2 * my_constants.DELTA_Y, 0, my_constants.DELTA_Y):
            Pad.spawn_pad(Pad, x_input=4, y_input=y)

    def update(self, delta_time):
        # update the list of pad's y-positions
        Pad.y_values_list = np.array([pad.center_y for pad in Pad.list])

        # if the player moves below the pad, then kill player
        if self.center_y - gameview_file.GameView.player_sprite.center_y > 5:
            gameview_file.GameView.player_dead = True

        # find pads that the player will hit
        self.hit_list = arcade.check_for_collision_with_list(
            gameview_file.GameView.player_sprite, Pad.list
        )
        # if the player hits a pad, then bounce player and move pad down.
        if len(self.hit_list) > 0:
            for hit_pad in self.hit_list:
                # there is probably a more efficient way of doing this.

                # re-position the pad.
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
                gameview_file.GameView.player_sprite.velocity *= (
                    -my_constants.BOUNCE_DECAY_CONSTANT
                )

                # add to score
                gameview_file.GameView.score += 1 * gameview_file.GameView.score_factor
                gameview_file.GameView.time_factor += my_constants.TIME_FACTOR_CHANGE
