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
        """you probably need to delete all of this code and then test it line by line because its currently untested, and it probably won't work."""
        #  if the player hits a target, then increase the score multiplier
        # find pads that the player will hit
        Target.hit_list = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Target.list
        )
        # if player hits pad, then:
        if len(Target.hit_list) > 0:
            for hit_target in Target.hit_list:
                if hit_target in Target.list:
                    # remove from sprite list to make sure that player interacts with target once
                    hit_target.remove_from_sprite_lists()

                    # increase score multiplier
                    gameview_file.GameView.score_factor += 1

    # MAJOR BUGS HERE. NOTE:
    output_hit_list = item_file.collision_detect(
        list1=player_file.Player.sprite, list2=Target.list
    )

    def test_function(hit_target_input):
        for hit_target in output_hit_list:
            if hit_target in Target.list:
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
