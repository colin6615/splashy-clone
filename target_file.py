"""holds the target class and dictionary"""

import arcade

import item_file
import player_file


class Target(item_file.Item):
    """
    If player hits a target, then the score multipler increases.

    Class Attributes:
        list (SpriteList): list of all pad sprites

    Instance Attributes:
    """

    def setup():
        """Set up the game and initialize the variables."""
        Target.list = arcade.SpriteList()

    def _update(self, delta_time):
        #  if the player hits a target, then increase the score multiplier
        # find pads that the player will hit
        Target.hit_list = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Target.list
        )
        # if player hits pad, then:
        if len(Target.hit_list) > 0:
            for hit_target in Target.hit_list:
                # remove from sprite list to make sure that player interacts with target once
                hit_target.remove_from_sprite_lists()

                # increase score multiplier
                gameview_file.GameView.score_factor += 1


import gameview_file

pad_dict = {
    "image_path": "assets/green_rectangle.png",
    "image_scale": 0.5,
    "Input_class": Target,
}
