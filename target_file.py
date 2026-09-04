"""holds the Target class and setup() function

It also adds the "input class" key to the target dictionary.
"""

import arcade

import item_file
import my_constants
import player_file


class Target(item_file.Item):
    """
    If player hits a target, then the score multipler increases and the target dissapears.

    Class Attributes:
        list (SpriteList): list of all pad sprites

    Instance Attributes:
    """

    def _update(self, delta_time):
        """If the player hits a target, then increase the score multiplier and delete the target"""
        # next few lines: if player hits pad, then for each colliding target:
        Target.colliding_player_and_target = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Target.list
        )
        if len(Target.colliding_player_and_target) > 0:
            for colliding_sprite in Target.colliding_player_and_target:
                # remove target from sprite list to make sure that player interacts with target once
                if colliding_sprite in Target.list:
                    colliding_sprite.remove_from_sprite_lists()

                    # increase score multiplier
                    gameview_file.GameView.score_factor += 1


def setup():
    """Set up the game and initialize the variables."""
    Target.list = arcade.SpriteList()


my_constants.target["Input_class"] = Target

import gameview_file
