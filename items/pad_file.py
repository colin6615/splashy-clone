"""holds the Pad class. Defines the spawn_pad() function.

This file also adds the "input class" key to the pad dictionary.

"""

import itertools
import random
from operator import attrgetter

import arcade

import camera_file
import items.coin_file
import items.item_file
import items.target_file
import my_constants
from items import player_file

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
    """

    def setup():
        """create sprite list. spawn the first 5 pads. Initialize other values."""
        # add bounds for pads x-position, so that the pads don't spawn off screen. The player can't bounce on pads if they are completely off screen.
        my_constants.pad["x_max"] = int(
            camera_file.My_camera.internal_width - my_constants.pad["width"] / 2
        )
        my_constants.pad["x_min"] = int(my_constants.pad["width"] / 2)

        Pad.list = arcade.SpriteList()

        # spawn the first 5 pads
        for y in range(-5, 0):
            Pad.spawn_pad(
                # first pads have random x position within the bounds
                x_=random.randrange(
                    my_constants.pad["start_x_min"], my_constants.pad["start_x_max"]
                ),
                # pad y-positions are delta_y apart
                y_=y * my_constants.pad["delta_y"],
            )

        player_file.Player.update_acceleration_factor()
        Pad.underneath_pad_duration = 0

    def update(self, delta_time):
        """Does stuff when the player bounces on, or moves below, a pad.
        Args:
            delta_time (float): time between ticks or updates. Unit is seconds. Default is 1/60 seconds.
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

                # if the pad is touching a target, then reset score factor to 1.
                target_pad_collision_list = arcade.check_for_collision_with_list(
                    hit_pad, items.target_file.Target.list
                )
                if len(target_pad_collision_list) > 0:
                    gameview_file.GameView.score_factor = 1

                # get positions of the new pad.
                new_center_x, new_center_y = position_pad()

                # create new pad
                Pad.spawn_pad(
                    x_=new_center_x,
                    y_=new_center_y,
                )

                # increase bounce count and score
                player_file.Player.bounce_count += 1
                gameview_file.GameView.score += gameview_file.GameView.score_factor

                # refresh acceleration factor because it changes with every bounce
                player_file.Player.update_acceleration_factor()

                # play sound
                arcade.play_sound(my_constants.pad["sound"])

                # delete items on pad
                # for each thing in items_close_to_pad, remove it
                while len(hit_pad.items_close_to_pad) > 0:
                    for pad_item_ in hit_pad.items_close_to_pad:
                        pad_item_.remove_from_sprite_lists()

                # delete the hit pad
                hit_pad.remove_from_sprite_lists()

        # find out if player is below a pad
        top_pad = max(Pad.list, key=attrgetter("center_y"))
        player_underneath_pad = (
            top_pad.center_y - player_file.Player.sprite.center_y > 0
        )

        # if player goes underneath a pad, during non-party, for 2 ticks, then kill them
        if player_underneath_pad and not items.coin_file.Coin.party:
            Pad.underneath_pad_duration += 1
        else:
            Pad.underneath_pad_duration = 0

        if Pad.underneath_pad_duration >= 2:
            gameview_file.GameView.dead = True

        # if player goes underneath a pad during party, don't kill them. teleport them above the pad because I don't want them to die during a party.
        if player_underneath_pad and items.coin_file.Coin.party:
            player_file.Player.sprite.center_y = (
                top_pad.center_y + player_file.Player.sprite.velocity_y
            )

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

        # alternate the pad sprite between image_path_1 and image_path_2
        # the first, second, and third pads use image_path_1, image_path_2, and image_path_1, respectively.

        im1 = my_constants.pad["image_path_1"]
        im2 = my_constants.pad["image_path_2"]

        # Source - https://stackoverflow.com/a/68037701
        # Posted by Zachiah
        # Retrieved 2026-09-13, License - CC BY-SA 4.0
        my_constants.pad["image_path"] = (
            im1 if my_constants.pad["image_path"] == im2 else im2
        )

        # create a list of everything spawned on this pad AKA the pad created by this call of spawn_pad()
        spawned_pad.items_close_to_pad = arcade.SpriteList()

        # spawn items on pad
        # source for next 2 loc:  https://stackoverflow.com/a/3203121
        # Posted by SilentGhost, modified by community. See post 'Timeline' for change history
        # Retrieved 2026-09-03, License - CC BY-SA 4.0
        for item_dict in items_close_to_pad_dicts:
            if random.random() < item_dict["spawn_rate"]:
                # calculate spawned item's y-position. item will spawn above pad.
                item_y = y_ + item_dict["height from pad"]

                # Make sure that the item doesn't overlap with another item
                # Boolean variable if we successfully placed the item.
                item_placed_successfully = False
                # Keep trying until success.
                while not item_placed_successfully:
                    # calculate bounds of spawned item's x-position
                    # items can spawn within spawn_radius from the pad center.

                    # if spawn_radius = my_constants.pad["width"] / 2 - item_dict["width"] / 2
                    # , then the item lies on the pad. Item's left edge cannot go further left than the pad's left edge.
                    # i changed the 2 to a 3 so that the item can hang off the pad a little bit.

                    # force spawn_radius to be positive, so that random.randrange() works.
                    spawn_radius = abs(
                        my_constants.pad["width"] / 2 - item_dict["width"] / 3
                    )
                    left_bound = int(x_ - spawn_radius)
                    right_bound = int(x_ + spawn_radius)

                    # generate item's x-position within the bounds
                    item_x = random.randrange(left_bound, right_bound)

                    # create sprite
                    spawned_item = items.item_file.spawn(
                        x_input=item_x,
                        y_input=item_y,
                        **item_dict,
                    )
                    # the last check is to make sure that the items don't overlap with each other. If you pass this last check, then break out of the loop.

                    item_hit_list = arcade.check_for_collision_with_list(
                        spawned_item, spawned_pad.items_close_to_pad
                    )
                    if len(item_hit_list) == 0:
                        item_placed_successfully = True
                # add spawned sprite to a list of items close to the pad. we use this in the Pad class.
                spawned_pad.items_close_to_pad.append(spawned_item)

                # fetch the item's class
                class_ = item_dict["Input_class"]

                class_.list.append(spawned_item)


import gameview_file

my_constants.pad["Input_class"] = Pad


def position_pad():
    """generates a position for a new pad. This position is below the bottom pad, but the x-position is slightly different (than the bottom pad).

    returns:
        dummy_center_x (int): horizontal position of new pad.
        dummy_center_y (int): horizontal position of vertical pad.
    """
    # generate pad's x-position, but make sure that we don't touch the screen's edges.
    pad_placed_successfully = False
    bottom_pad = min(Pad.list, key=attrgetter("center_y"))

    while not pad_placed_successfully:
        # add a random number to x-position of bottom pad.
        x_change = random.randrange(
            -my_constants.pad["delta_x"], my_constants.pad["delta_x"]
        )

        dummy_center_x = bottom_pad.center_x + x_change

        # if the pad is not touching the screen's edges, then pad was succesfully placed.
        if (
            dummy_center_x > my_constants.pad["x_min"]
            and dummy_center_x < my_constants.pad["x_max"]
        ):
            pad_placed_successfully = True
    # after you successfully change the x-position, get y-position, which is below the bottom pad.
    dummy_center_y = bottom_pad.center_y - my_constants.pad["delta_y"]
    return dummy_center_x, dummy_center_y
