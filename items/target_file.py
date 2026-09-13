"""holds the Target class and setup() function

It also adds the "input class" key to the target dictionary.
"""

import arcade

import items.item_file
import items.player_file as player_file
import my_constants


class Target(items.item_file.Item):
    """
    If player hits a target, then the score multipler increases and the target dissapears.

    Class Attributes:
        list (SpriteList): list of all target sprites

    Instance Attributes:
    """

    def update(self, delta_time):
        """
        Args:
            delta_time (float): time between ticks or updates. Unit is seconds. Default is 1/60 seconds.
        If the player hits a target, then increase the score multiplier and delete the target"""
        # next few lines: if player hits pad, then for remove target from sprite list to make sure that player interacts with target once
        self.colliding_player_and_target = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Target.list
        )
        for colliding_sprite in self.colliding_player_and_target:
            if colliding_sprite in Target.list:
                colliding_sprite.remove_from_sprite_lists()

                gameview_file.GameView.score_factor += 1
                arcade.play_sound(my_constants.target["sound"])

    def setup():
        """Set up the game and initialize the variables."""
        Target.list = arcade.SpriteList()


my_constants.target["Input_class"] = Target

import gameview_file
