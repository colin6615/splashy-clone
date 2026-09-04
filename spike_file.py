"""holds the Spike class and setup() function

It also adds the "input class" key to the spike dictionary.
"""

import arcade

import gameview_file
import item_file
import my_constants
import player_file


class Spike(item_file.Item):
    """
    If player hits a spike, then the spike count increases and the spike dissapears

    Class Attributes:
        list (SpriteList): list of all pad sprites

    Instance Attributes:
    """

    def _update(self, delta_time):
        """If the player hits a spike, then increase the score multiplier and delete the spike"""
        # next few lines: if player hits pad, then for each colliding spike:
        Spike.colliding_player_and_spike = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Spike.list
        )
        if len(Spike.colliding_player_and_spike) > 0:
            for colliding_sprite in Spike.colliding_player_and_spike:
                # remove spike from sprite list to make sure that player interacts with spike once
                if colliding_sprite in Spike.list:
                    gameview_file.GameView.dead = True


def setup():
    """Set up the game and initialize the variables."""
    Spike.list = arcade.SpriteList()
    Spike.count_count = 0


my_constants.spike["Input_class"] = Spike
