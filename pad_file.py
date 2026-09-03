"""holds the pad class and dictionary

Pad dictionary is only used by the pad class.
"""

import random
from operator import attrgetter

import arcade

import item_file
import my_constants
import player_file
import target_file

# --- Constants ---
# the first 4 pads will spawn with x values in between these two bounds
# Currently, the bounds enclose the middle one third of the screen
STARTING_PADS_LEFT_BOUND = int(my_constants.WINDOW_WIDTH / 3)
STARTING_PADS_RIGHT_BOUND = int(my_constants.WINDOW_WIDTH * 2 / 3)

# Kill the player after they go MIN_PLAYER_PAD_HEIGHT_DIFFERENCE pixels underneath a pad.
MIN_PLAYER_PAD_HEIGHT_DIFFERENCE = 0
# ==================


class Pad(item_file.Item):
    """
    If player hits a pad, then the player bounces and the pad respawns below them.

    Class Attributes:
        list (SpriteList): list of all pad sprites

    Instance Attributes:
    """

    def setup():
        """Set up the game and initialize the variables."""
        Pad.list = arcade.SpriteList()

        # spawn the first 4 pads
        for y in range(-4, 0):
            item_file.spawn(
                # first pads have random x position within the bounds
                x_input=random.randrange(
                    STARTING_PADS_LEFT_BOUND, STARTING_PADS_RIGHT_BOUND
                ),
                y_input=y * my_constants.DELTA_Y,
                **pad_dict,  # defined at the bottom of this file
            )

    def _update(self, delta_time):
        # kill the player if they go below the top pad
        top_pad = max(Pad.list, key=attrgetter("center_y"))
        if (
            top_pad.center_y - player_file.Player.sprite.center_y
            > MIN_PLAYER_PAD_HEIGHT_DIFFERENCE
        ):
            gameview_file.GameView.dead = True
        # ---------------- For pads that the player hits.
        # find pads that the player will hit
        self.hit_list = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Pad.list
        )
        # ---------------- if the player hits a pad, then move the pad and bounce player.
        if len(self.hit_list) > 0:
            for hit_pad in self.hit_list:
                # ------------ if the pad is touching a target, then reset score factor
                # Find hit pads touching a targets
                # I'm not sure if hit_pad needs to be a sprite list, or if its okay for hit_pad to be just a single sprite as a parameter in check_for_collision_with_list()
                target_pad_collision_list = arcade.check_for_collision_with_list(
                    hit_pad, target_file.Target.list
                )

                if len(target_pad_collision_list) > 0:
                    for target_and_pad in target_pad_collision_list:
                        gameview_file.GameView.score = 1

                # ------------ Start of re-position pad
                #  teleport hit pad directly below pad 4. Then change pad 1's x-position, slightly
                # ------------ randomize pad's x-position, but don't touch the screen's edges
                # Boolean variable if we successfully placed the pad.
                pad_placed_successfully = False
                # Keep trying until success.
                while not pad_placed_successfully:
                    # ----------------- Change this pad's x-position to the bottom pad, and then add a random number to this.
                    # generate random number to add later
                    x_change = random.randrange(
                        -my_constants.MOVE_PAD_X, my_constants.MOVE_PAD_X
                    )
                    # get bottom pad
                    bottom_pad = min(Pad.list, key=attrgetter("center_y"))
                    # add random number to bottom pad's x-position. Equate its value to the hit pad's x-position
                    hit_pad.center_x = bottom_pad.center_x + x_change

                    # if the pad is not touching the screen's edges, then pad was succesfully placed.
                    right_edge = my_constants.WINDOW_WIDTH - my_constants.PAD_LENGTH
                    if (
                        hit_pad.center_x > my_constants.PAD_LENGTH
                        and hit_pad.center_x < right_edge
                    ):
                        pad_placed_successfully = True
                # ------------- after you successfully change the x-position
                # move pad down
                hit_pad.center_y = bottom_pad.center_y - my_constants.DELTA_Y
                # ------------------- End of re-position pad

                # bounce player
                player_file.Player.sprite.velocity *= (
                    -my_constants.BOUNCE_DECAY_CONSTANT
                )

                # increase time factor and score
                gameview_file.GameView.time_factor += my_constants.TIME_FACTOR_CHANGE
                gameview_file.GameView.score += gameview_file.GameView.score_factor


import gameview_file

pad_dict = {
    "image_path": "assets/green_rectangle.png",
    "image_scale": 0.5,
    "Input_class": Pad,
}
