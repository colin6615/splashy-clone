"""holds the Pad class. Defines the spawn_pad() function.

This file also adds the "input class" key to the pad dictionary.

"""

import random
from operator import attrgetter

import arcade

import items.item_file
import items.player_file as player_file
import items.target_file
import my_constants

# list of item dictionaries used later.
# NOTE: excludes pad
items_close_to_pad_dicts = [
    my_constants.target,
    my_constants.coin,
    my_constants.spike,
]


class Pad(items.item_file.Item):
    """
    If player hits a pad, then the player bounces and the pad respawns below them.

    Class Attributes:
        list (SpriteList): list of all pad sprites

    Instance Attributes:
    """

    def setup():
        """create sprite list and spawn the first pads"""
        # add bounds for pads
        my_constants.pad["x_max"] = int(
            gameview_file.GameView.internal_width - my_constants.pad["width"] / 2
        )
        my_constants.pad["x_min"] = int(my_constants.pad["width"] / 2)

        Pad.list = arcade.SpriteList()
        # spawn the first 4 pads
        for y in range(-4, 0):
            spawn_pad(
                # first pads have random x position within the bounds
                x_=random.randrange(
                    my_constants.pad["start_x_min"], my_constants.pad["start_x_max"]
                ),
                y_=y * my_constants.pad["delta_y"],
            )
        gameview_file.GameView.update_game_speed()

    def update(self, delta_time):
        """
        Args:
            delta_time (int): framerate in hertz. how many times per second that the game updates.
        """
        # whole seciton: if player hits a pad, then bounce player, remove pad, create new pad, and change score
        # next few lines: if player hits a pad, then:
        self.hit_list = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Pad.list
        )
        for hit_pad in self.hit_list:
            if hit_pad in Pad.list:
                # bounce player
                player_file.Player.sprite.velocity_y *= (
                    -my_constants.BOUNCE_DECAY_CONSTANT
                )

                # if the pad is touching a target, then reset score factor
                target_pad_collision_list = arcade.check_for_collision_with_list(
                    hit_pad, items.target_file.Target.list
                )
                if len(target_pad_collision_list) > 0:
                    gameview_file.GameView.score_factor = 1

                # ------------ Start of re-position pad
                #  In this whole section, I teleport hit pad directly below the bottom pad. Then change the hit pad's x-position, slightly
                # First, randomize pad's x-position, but make sure that we don't touch the screen's edges. I achieve this thorugh the following loc
                # Boolean variable if we successfully placed the pad.
                pad_placed_successfully = False
                # Keep trying until success.

                # get bottom pad
                bottom_pad = min(Pad.list, key=attrgetter("center_y"))
                while not pad_placed_successfully:
                    # ----------------- Change this pad's x-position to the bottom pad, and then add a random number to this.
                    # generate random number to add later
                    x_change = random.randrange(
                        -my_constants.pad["delta_x"], my_constants.pad["delta_x"]
                    )
                    # add random number to bottom pad's x-position. Equate its value to the hit pad's x-position
                    new_center_x = bottom_pad.center_x + x_change

                    # if the pad is not touching the screen's edges, then pad was succesfully placed.
                    if (
                        new_center_x > my_constants.pad["x_min"]
                        and new_center_x < my_constants.pad["x_max"]
                    ):
                        pad_placed_successfully = True
                # ------------- after you successfully change the x-position
                # move pad down
                new_center_y = bottom_pad.center_y - my_constants.pad["delta_y"]
                # ------------------- End of re-position pad

                # create new pad
                spawn_pad(
                    x_=new_center_x,
                    y_=new_center_y,
                )

                # increase bounce count and score
                gameview_file.GameView.bounce_count += 1
                gameview_file.GameView.score += gameview_file.GameView.score_factor

                # refresh values that change with bounce
                gameview_file.GameView.update_game_speed()

                # play sound
                arcade.play_sound(my_constants.pad["sound"])

                # delete items on pad
                # for each thing in items_close_to_pad, remove it
                while len(hit_pad.items_close_to_pad) > 0:
                    for pad_item_ in hit_pad.items_close_to_pad:
                        pad_item_.remove_from_sprite_lists()

                # delete the hit pad
                hit_pad.remove_from_sprite_lists()

        # kill the player if they go below the top pad
        # find top pad
        top_pad = max(Pad.list, key=attrgetter("center_y"))

        # get height difference between pad and player
        player_pad_height_difference = (
            top_pad.center_y - player_file.Player.sprite.center_y
        )
        # create thresholds that describe how far the player goes underneath the pad.
        slightly_below_top_pad = player_pad_height_difference > 5
        way_below_top_pad = player_pad_height_difference > 500

        # kill the player if they cross the current threshold

        if slightly_below_top_pad and not gameview_file.GameView.party:
            gameview_file.GameView.dead = True
        if way_below_top_pad and gameview_file.GameView.party:
            gameview_file.GameView.dead = True


import gameview_file

my_constants.pad["Input_class"] = Pad


def spawn_pad(
    x_,
    y_,
):
    """
    spawns a pad at the specified coordinates
    Each item type has a chance to spawn on said pad (which was created using this function)

    args
        x_ (int): y-coordinate of center of spawned pad
        y_ (int): x-coordinate of center of spawned pad
    """
    spawned_pad = items.item_file.spawn(
        x_input=x_,
        y_input=y_,
        **my_constants.pad,
    )
    Pad.list.append(spawned_pad)

    # create a list of everything spawned on this pad AKA the pad created by this call of spawn_pad()
    spawned_pad.items_close_to_pad = arcade.SpriteList()

    # source for next 2 loc:  https://stackoverflow.com/a/3203121
    # Posted by SilentGhost, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-09-03, License - CC BY-SA 4.0
    for item_dict in items_close_to_pad_dicts:
        if random.random() < item_dict["spawn_rate"]:
            # calculate spawned item's y-position
            item_y = y_ + item_dict["height from pad"]

            # Make sure that the item doesn't overlap with another item
            # Boolean variable if we successfully placed the item.
            item_placed_successfully = False
            # Keep trying until success.
            while not item_placed_successfully:
                # calculate bounds of spawned item's x-position
                # if temp length = my_constants.pad["width"] / 2 - item_dict["width"] / 2
                # , then the item lies on the pad. Item's left edge cannot go further left than the pad's left edge.
                # i changed the 2 to a 4 so that the item can hang off the pad a little bit.
                temp_length_1 = my_constants.pad["width"] / 2 - item_dict["width"] / 4
                # take the maximum value of 2 lengths. If the item widths are much larger han the pad width, then left_bound > right_bound. So the random.randrange() function (a few loc below this line) doesn't work; the spawn function doesn't work.
                # avoid this situation by forcing temp_length to be positive.
                temp_length_2 = my_constants.pad["width"] / 2
                temp_length = max(temp_length_1, temp_length_2)
                left_bound = int(x_ - temp_length)
                right_bound = int(x_ + temp_length)

                # generate item's x-position within the bounds
                item_x = random.randrange(left_bound, right_bound)

                # create sprite
                spawned_item = items.item_file.spawn(
                    x_input=item_x,
                    y_input=item_y,
                    **item_dict,
                )
                # NOTE: try to make spawn something. return spawned_item as a proposal sprite
                # NOTE: call item_file.spawn()
                # check if the item collides with another item.
                # First, find items that are colliding
                item_hit_list = arcade.check_for_collision_with_list(
                    spawned_item, spawned_pad.items_close_to_pad
                )
                # if the hit list is empty (no items are colliding), then break out of this while loop
                if len(item_hit_list) == 0:
                    item_placed_successfully = True
            # add spawned sprite to a list of items close to the pad
            spawned_pad.items_close_to_pad.append(spawned_item)

            # fetch the item's class
            class_ = item_dict["Input_class"]

            # add the spawned sprite to its classes spritelist
            class_.list.append(spawned_item)
