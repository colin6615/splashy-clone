import random

import arcade
import numpy as np

import main
import my_constants


class Pad(arcade.SpriteList):
    def spawn_pad(x_input, y_input):
        """
        spawns a 3x1 structure of pads.
        Args:
            x (int): the x-position of the center of one of the pads (I'm not sure which pad it is). Units are in terms of pads. If you drew a line from x=0 to x=2, then it has length of 2 * PAD_LENGTH. I don't know what the PAD_LENGTH is.

            y (int): the y-position of the center of all of the pads. Units are in terms of pads.

        Returns:
            Return (type): What is returned and why.

        """
        pad = arcade.Sprite(
            "assets/green_rectangle.png", my_constants.SPRITE_SCALING_PAD
        )
        # position the pad
        pad.center_x = x_input * my_constants.PAD_LENGTH
        pad.center_y = y_input * my_constants.PAD_LENGTH
        Pad.list.append(pad)
        Pad.y_values_list = np.array([pad.center_y for pad in Pad.list])

    def __init__(self):
        Pad.list = None
        Pad.y_values_list = None

    def setup():
        """Set up the game and initialize the variables."""

        # Sprite lists
        Pad.list = arcade.SpriteList()
        Pad.y_values_list = []
        # spawn the first 2 pads
        for y in range(-2 * my_constants.DELTA_Y, 0, my_constants.DELTA_Y):
            Pad.spawn_pad(x_input=4, y_input=y)

    def update():
        # if a pad is above the player, then end the game
        for pad3 in Pad.list:
            if pad3.center_y - gameview_file.GameView.player_sprite.center_y > 5:
                main.Testy.game_over_function()
                

        # find pads that the player will hit
        pad_hit_list = arcade.check_for_collision_with_list(
            gameview_file.GameView.player_sprite, Pad.list
        )
        # if the player hits a pad, then bounce player and move pad down.
        if len(pad_hit_list) > 0:
            for pad2 in pad_hit_list:
                # there is probably a more efficient way of doing this.
                # update the list of pad's y-positions
                Pad.y_values_list = np.array([pad.center_y for pad in Pad.list])
                # re-position the pad.
                # move pad down
                pad2.center_y = (
                    min(Pad.y_values_list)
                    - my_constants.DELTA_Y * my_constants.PAD_LENGTH
                )
                # randomize pad's x-position
                pad2.center_x += random.randrange(
                    -my_constants.MOVE_PAD_X, my_constants.MOVE_PAD_X
                )

                # update the list of pad's y-positions
                Pad.y_values_list = np.array([pad.center_y for pad in Pad.list])
                # bounce player
                gameview_file.GameView.player_sprite.velocity *= (
                    -my_constants.BOUNCE_DECAY_CONSTANT
                )

                # add to score
                gameview_file.GameView.score += 1 * gameview_file.GameView.score_factor
                gameview_file.GameView.time_factor += my_constants.TIME_FACTOR_CHANGE


import gameview_file
