"""holds the Coin class and setup() function
It also adds the "input class" key to the coin dictionary.
"""

import arcade

import gameview_file
import item_file
import my_constants
import pad_file
import player_file
import spike_file
import target_file


class Coin(item_file.Item):
    """
    If player hits a coin, then the coin count increases and the coin dissapears

    Class Attributes:
        list (SpriteList): list of all coin sprites

    Instance Attributes:
    """

    def _update(self, delta_time):
        """If the player hits a coin, then increase the score multiplier and delete the coin"""
        # next few lines: if player hits coin, then for each colliding coin:
        Coin.colliding_player_and_coin = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Coin.list
        )
        if len(Coin.colliding_player_and_coin) > 0:
            for colliding_sprite in Coin.colliding_player_and_coin:
                # remove coin from sprite list to make sure that player interacts with coin once
                if colliding_sprite in Coin.list:
                    colliding_sprite.remove_from_sprite_lists()

                    # increase coin score
                    Coin.score += 1
        # when the player gets 10 coins:
        SECONDS_PER_PARTY = (
            40  # duration of party. value of 40 makes about 10 seconds of party
        )
        COINS_PER_TICK = (
            0.1  # how many coins are added to the coin count every tick during party.
        )
        TICKS_PER_SECOND = 60
        COIN_CHANGE_PER_PARTY = SECONDS_PER_PARTY * TICKS_PER_SECOND * COINS_PER_TICK
        right_bound = my_constants.coin["max"] + COIN_CHANGE_PER_PARTY
        if (Coin.score >= my_constants.coin["max"]) and (Coin.score <= right_bound):
            gameview_file.GameView.party = True
            # set time_factor and time_factor_change to their party modes
            gameview_file.GameView.time_factor_change = (
                gameview_file.GameView.TIME_FACTOR_CHANGE_MANAGER["party"]
            )
            gameview_file.GameView.time_factor = (
                gameview_file.GameView.time_factor_party
            )
            # increase coin count
            Coin.score += COINS_PER_TICK
            # remove all spikes
            for spike in spike_file.Spike.list:
                spike.remove_from_sprite_lists()

            # if its party time, then align the
            if gameview_file.GameView.party == True:
                for pad in pad_file.Pad.list:
                    pad.center_x = player_file.Player.sprite.center_x
                for target in target_file.Target.list:
                    target.center_x = player_file.Player.sprite.center_x
        if Coin.score > right_bound:
            # reset coin count
            Coin.score = 0
            gameview_file.GameView.party = False
            # set time_factor and time_factor_change to their non_party modes
            gameview_file.GameView.time_factor_change = (
                gameview_file.GameView.TIME_FACTOR_CHANGE_MANAGER["not_party"]
            )
            gameview_file.GameView.time_factor = (
                gameview_file.GameView.time_factor_not_party
            )


def setup():
    """Set up the game and initialize the variables."""
    Coin.list = arcade.SpriteList()
    Coin.score = 0
    Coin.party = False


my_constants.coin["Input_class"] = Coin
