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

    def _update(self, delta_time):
        """you probably need to delete all of this code and then test it line by line because its currently untested, and it probably won't work."""
        # this section: if the player hits a target, then increase the score multiplier and delete the target
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


import gameview_file

spawn_dict = {
    "image_path": "assets/target.png",
    "image_scale": 1,
    "Input_class": Target,
}
