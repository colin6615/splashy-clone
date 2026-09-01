"""holds the pad/trapoline class"""

import random
from operator import attrgetter

import arcade

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

    # make it so the random numbers generated in this class are the same in every run of the game.
    random.seed(10)  # remove upon release

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
        pad.center_x = x_input
        pad.center_y = y_input

        Pad.list.append(pad)

    def setup():
        """Set up the game and initialize the variables."""

        Pad.list = None
        Pad.list = arcade.SpriteList()

        # spawn the first 4 pads
        for y in range(-4, 0):
            Pad.spawn_pad(
                x_input=random.randrange(
                    int(my_constants.WINDOW_WIDTH / 3),
                    int(my_constants.WINDOW_WIDTH * 2 / 3),
                ),
                y_input=y * my_constants.DELTA_Y * my_constants.PAD_LENGTH,
            )

    def update():

        # kill the player if they go below the top pad
        top_pad = max(Pad.list, key=attrgetter("center_y"))
        if top_pad.center_y - player_file.Player.sprite.center_y > 5:
            gameview_file.GameView.dead = True

        # find pads that the player will hit
        hit_list = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Pad.list
        )
        # if the player hits a pad, then bounce player and move the pad.
        # there is probably a more efficient way of writing the next 2 loc.
        if len(hit_list) > 0:
            for hit_pad in hit_list:
                # move pad down
                hit_pad.center_y = (
                    min(Pad.y_values_list)
                    - my_constants.DELTA_Y * my_constants.PAD_LENGTH
                )
                # get the x-position of next pad

                # get the new top pad (this is the pad that the player is about to hit!)

                # randomize pad's x-position
                # Boolean variable if we successfully placed the pad .
                pad_placed_successfully = False
                # Keep trying until success.
                while not pad_placed_successfully:
                    # randomize pad's x-position
                    x_change = random.randrange(
                        -my_constants.MOVE_PAD_X, my_constants.MOVE_PAD_X
                    )
                    hit_pad.center_x += x_change

                    # if the pad is not touching the screen's edges, then pad was succesfully placed.
                    right_edge = my_constants.WINDOW_WIDTH - my_constants.PAD_LENGTH
                    if (
                        hit_pad.center_x > my_constants.PAD_LENGTH
                        and hit_pad.center_x < right_edge
                    ):
                        pad_placed_successfully = True
                        print(x_change)

                # bounce player
                player_file.Player.sprite.velocity *= (
                    -my_constants.BOUNCE_DECAY_CONSTANT
                )

                # add to score
                gameview_file.GameView.score += 1 * gameview_file.GameView.score_factor
                gameview_file.GameView.time_factor += my_constants.TIME_FACTOR_CHANGE


import gameview_file
