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
        """create sprite list and spawn the first pads"""
        Pad.list = arcade.SpriteList()

        # spawn the first 4 pads
        for y in range(-4, 0):
            spawn_pad(
                # first pads have random x position within the bounds
                x_=random.randrange(
                    STARTING_PADS_LEFT_BOUND, STARTING_PADS_RIGHT_BOUND
                ),
                y_=y * my_constants.DELTA_Y,
            )

    def _update(self, delta_time):
        # kill the player if they go below the top pad
        top_pad = max(Pad.list, key=attrgetter("center_y"))
        if (
            top_pad.center_y - player_file.Player.sprite.center_y
            > MIN_PLAYER_PAD_HEIGHT_DIFFERENCE
        ):
            gameview_file.GameView.dead = True
        # whole seciton: if player hits a pad, then bounce player, remove pad, create new pad, and change score
        # next few lines: if player hits a pad, then:
        self.hit_list = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Pad.list
        )
        if len(self.hit_list) > 0:
            for hit_pad in self.hit_list:
                # if the pad is touching a target, then reset score factor
                target_pad_collision_list = arcade.check_for_collision_with_list(
                    hit_pad, target_file.Target.list
                )
                if len(target_pad_collision_list) > 0:
                    for target_and_pad in target_pad_collision_list:
                        gameview_file.GameView.score_factor = 1

                # delete items on pad
                # for each thing in items_close_to_pad, remove it
                for pad_item in hit_pad.items_close_to_pad:
                    pad_item.remove_from_sprite_lists()

                # delete the hit pad
                hit_pad.remove_from_sprite_lists()

                # ------------ Start of re-position pad
                #  In this whole section, I teleport hit pad directly below the bottom pad. Then change the hit pad's x-position, slightly
                # First, randomize pad's x-position, but don't touch the screen's edges
                # Boolean variable if we successfully placed the pad.
                pad_placed_successfully = False
                # Keep trying until success.

                # get bottom pad
                bottom_pad = min(Pad.list, key=attrgetter("center_y"))
                while not pad_placed_successfully:
                    # ----------------- Change this pad's x-position to the bottom pad, and then add a random number to this.
                    # generate random number to add later
                    x_change = random.randrange(
                        -my_constants.MOVE_PAD_X, my_constants.MOVE_PAD_X
                    )
                    # add random number to bottom pad's x-position. Equate its value to the hit pad's x-position
                    new_center_x = bottom_pad.center_x + x_change

                    # if the pad is not touching the screen's edges, then pad was succesfully placed.
                    right_edge = my_constants.WINDOW_WIDTH - my_constants.PAD_LENGTH
                    left_edge = my_constants.PAD_LENGTH
                    if new_center_x > left_edge and new_center_x < right_edge:
                        pad_placed_successfully = True
                # ------------- after you successfully change the x-position
                # move pad down
                new_center_y = bottom_pad.center_y - my_constants.DELTA_Y
                # ------------------- End of re-position pad

                # create new pad
                spawn_pad(
                    x_=new_center_x,
                    y_=new_center_y,
                )

                # bounce player
                player_file.Player.sprite.velocity *= (
                    -my_constants.BOUNCE_DECAY_CONSTANT
                )

                # increase time factor and score
                gameview_file.GameView.time_factor += my_constants.TIME_FACTOR_CHANGE
                gameview_file.GameView.score += gameview_file.GameView.score_factor


import gameview_file

dict = {
    "image_path": "assets/green_rectangle.png",
    "image_scale": 0.5,
    "Input_class": Pad,
}
item_dicts = [dict, target_file.dict]


def spawn_pad(
    x_,
    y_,
):
    """
    spawns a pad at the specified coordinates
    spawns a target on the pad.
    the target should have same y-input, but different x_
    """
    spawned_pad = item_file.spawn(
        x_input=x_,
        y_input=y_,
        **dict,  # the item is a pad.
    )

    # create a list of everything spawned on this pad AKA the pad created by this call of spawn_pad()
    spawned_pad.items_close_to_pad = []

    # source for next 2 loc:  https://stackoverflow.com/a/3203121
    # Posted by SilentGhost, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-09-03, License - CC BY-SA 4.0

    # 30% of the time, a target spawns
    percentage_chance = 0.3  # 30% chance

    if random.random() < percentage_chance:
        left_bound = int(x_ - my_constants.PAD_LENGTH / 2)
        right_bound = int(x_ + my_constants.PAD_LENGTH / 2)
        target_x = random.randrange(left_bound, right_bound)
        # create the target sprite
        spawned_target = item_file.spawn(
            x_input=target_x,
            y_input=y_,
            **target_file.dict,
        )
        # add target sprite to a list of items close to the pad
        spawned_pad.items_close_to_pad.append(spawned_target)
