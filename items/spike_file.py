"""holds the Spike class and setup() function

It also adds the "input class" key to the spike dictionary.
"""

import arcade

import gameview_file
import items.item_file
import items.player_file as player_file
import my_constants


class Spike(items.item_file.Item):
    """
    If player hits a spike, then the spike count increases and the spike dissapears

    Class Attributes:
        list (SpriteList): list of all spike sprites

    Instance Attributes:
    """

    def update(self, delta_time):
        """
        Args:
            delta_time (float): time between ticks or updates. Unit is seconds. Default is 1/60 seconds.
        if player hits spike, then kill the player"""
        Spike.colliding_player_and_spike = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Spike.list
        )
        if len(Spike.colliding_player_and_spike) > 0:
            # kill player
            gameview_file.GameView.dead = True

    def setup():
        """Set up the game and initialize the variables."""
        Spike.list = arcade.SpriteList()


my_constants.spike["Input_class"] = Spike
