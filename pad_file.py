"""holds the pad/trapoline class"""

import random
from operator import attrgetter

import arcade

import item_file
import my_constants
import player_file

# --- Constants ---
# the first 4 pads will spawn with x values in between these two bounds
# Currently, the bounds enclose the middle one third of the screen
STARTING_PADS_LEFT_BOUND = int(my_constants.WINDOW_WIDTH / 3)
STARTING_PADS_RIGHT_BOUND = int(my_constants.WINDOW_WIDTH * 2 / 3)

# Kill the player after they go MIN_PLAYER_PAD_HEIGHT_DIFFERENCE underneath a pad.
MIN_PLAYER_PAD_HEIGHT_DIFFERENCE = 0
# ==================


class Pad(item_file.Item):
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

    def spawn(x_input, y_input, image_path, image_scale):
        """
        spawns an item at specified coordinates

        Args:
            x_input (float): the x-position of the center of the spawned item.

            y_input (float): the y-position of the center of the spawned item.
        """
        # make item sprite
        item = Pad(
            image_path, image_scale
        )  # need some way to get self.image_path without calling self?

        # position the pad
        item.center_x = x_input
        item.center_y = y_input

        Pad.list.append(item)

    # def spawn_pad(x_input, y_input):
    #     """
    #     spawns pads.

    #     Units are in terms of pads. If you drew a line from x=0 to x=2, then it has length of 2 * PAD_LENGTH.

    #     Args:
    #         x_input (float): the x-position of the center of the spawned pad.

    #         y_input (float): the y-position of the center of the spawned pad.
    #     """
    #     # make pad sprite
    #     pad = Pad("assets/green_rectangle.png", my_constants.SPRITE_SCALING_PAD)

    #     # position the pad
    #     pad.center_x = x_input
    #     pad.center_y = y_input

    #     Pad.list.append(pad)

    def setup():
        """Set up the game and initialize the variables."""
        Pad.list = arcade.SpriteList()

        # spawn the first 4 pads
        for y in range(-4, 0):
            Pad.spawn(
                # first pads have random x position within the bounds
                x_input=random.randrange(
                    STARTING_PADS_LEFT_BOUND, STARTING_PADS_RIGHT_BOUND
                ),
                y_input=y * my_constants.DELTA_Y,
                image_path="assets/green_rectangle.png",
                image_scale=0.5,
                # CLASS=Pad,
            )
            """
            
            Pad.spawn_pad(
                # first pads have random x position within the bounds
                x_input=random.randrange(
                    STARTING_PADS_LEFT_BOUND, STARTING_PADS_RIGHT_BOUND
                ),
                y_input=y * my_constants.DELTA_Y,
            )
            """

    def _update(self, delta_time):
        # kill the player if they go below the top pad
        top_pad = max(Pad.list, key=attrgetter("center_y"))
        if (
            top_pad.center_y - player_file.Player.sprite.center_y
            > MIN_PLAYER_PAD_HEIGHT_DIFFERENCE
        ):
            gameview_file.GameView.dead = True

        # find pads that the player will hit
        self.hit_list = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Pad.list
        )
        # if the player hits a pad, then bounce player and move the pad.
        if len(self.hit_list) > 0:
            for hit_pad in self.hit_list:
                # get the bottom pad
                bottom_pad = min(Pad.list, key=attrgetter("center_y"))

                # randomize pad's x-position, but don't touch the screen's edges
                # Boolean variable if we successfully placed the pad.
                pad_placed_successfully = False
                # Keep trying until success.
                while not pad_placed_successfully:
                    # randomize pad's x-position
                    x_change = random.randrange(
                        -my_constants.MOVE_PAD_X, my_constants.MOVE_PAD_X
                    )
                    hit_pad.center_x = bottom_pad.center_x + x_change

                    # if the pad is not touching the screen's edges, then pad was succesfully placed.
                    right_edge = my_constants.WINDOW_WIDTH - my_constants.PAD_LENGTH
                    if (
                        hit_pad.center_x > my_constants.PAD_LENGTH
                        and hit_pad.center_x < right_edge
                    ):
                        pad_placed_successfully = True

                # move pad down
                hit_pad.center_y = bottom_pad.center_y - my_constants.DELTA_Y

                # bounce player
                player_file.Player.sprite.velocity *= (
                    -my_constants.BOUNCE_DECAY_CONSTANT
                )

                # add to score
                gameview_file.GameView.score += 1 * gameview_file.GameView.score_factor
                gameview_file.GameView.time_factor += my_constants.TIME_FACTOR_CHANGE


import gameview_file
