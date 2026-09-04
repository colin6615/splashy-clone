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
        list (SpriteList): list of all spike sprites

    Instance Attributes:
    """

    def _update(self, delta_time):
        """if player hits spike, then kill the player"""
        Spike.colliding_player_and_spike = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Spike.list
        )
        if len(Spike.colliding_player_and_spike) > 0:
            for colliding_sprite in Spike.colliding_player_and_spike:
                if colliding_sprite in Spike.list:
                    # kill player
                    gameview_file.GameView.dead = True


def setup():
    """Set up the game and initialize the variables."""
    Spike.list = arcade.SpriteList()


my_constants.spike["Input_class"] = Spike
