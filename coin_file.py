"""holds the Coin class and setup() function

It also adds the "input class" key to the coin dictionary.
"""

import arcade

import item_file
import my_constants
import player_file


class Coin(item_file.Item):
    """
    If player hits a coin, then the coin count increases and the coin dissapears

    Class Attributes:
        list (SpriteList): list of all pad sprites

    Instance Attributes:
    """

    def _update(self, delta_time):
        """If the player hits a coin, then increase the score multiplier and delete the coin"""
        # next few lines: if player hits pad, then for each colliding coin:
        Coin.colliding_player_and_coin = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Coin.list
        )
        if len(Coin.colliding_player_and_coin) > 0:
            for colliding_sprite in Coin.colliding_player_and_coin:
                # remove coin from sprite list to make sure that player interacts with coin once
                if colliding_sprite in Coin.list:
                    colliding_sprite.remove_from_sprite_lists()

                    # increase score multiplier
                    Coin.count_count += 1


def setup():
    """Set up the game and initialize the variables."""
    Coin.list = arcade.SpriteList()
    Coin.count_count = 0


my_constants.coin["Input_class"] = Coin
