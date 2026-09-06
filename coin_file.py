"""holds the Coin class and setup() function

This file also adds the "input class" key to the coin dictionary.
"""

import arcade

import gameview_file
import item_file
import my_constants
import pad_file
import player_file
import spike_file
import target_file

# First, calculate how many coins are added to the coin count during the party
COINS_PER_UPDATE = (
    0.1  # how many coins are added to the coin count every update during party.
)
UPDATES_PER_SECOND = 250
SECONDS_PER_PARTY = 6.5  # party duration in seconds
COIN_CHANGE_PER_PARTY = (
    UPDATES_PER_SECOND * SECONDS_PER_PARTY * COINS_PER_UPDATE
)  # how many coins are added to the coin count during the party


COINS_AFTER_PARTY = (
    my_constants.coin["max"] + COIN_CHANGE_PER_PARTY
)  # the maximum number of coins during a party. The coin count at the end of the party.


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
        # if the coin count is in the party range, then:
        if my_constants.coin["max"] <= Coin.score < COINS_AFTER_PARTY:
            # change stuff to their party counterparts
            gameview_file.GameView.party = True
            gameview_file.GameView.time_factor_change = (
                my_constants.TIME_FACTOR_CHANGE_MANAGER["party"]
            )
            gameview_file.GameView.time_factor = (
                gameview_file.GameView.time_factor_party
            )

            # increase coin count
            Coin.score += COINS_PER_UPDATE

            # remove spikes, so that the player doesn't die
            for spike in spike_file.Spike.list:
                spike.remove_from_sprite_lists()

            # move the pads and target to the player
            for pad in pad_file.Pad.list:
                pad.center_x = player_file.Player.sprite.center_x
            for target in target_file.Target.list:
                target.center_x = player_file.Player.sprite.center_x
            for coin in Coin.list:
                coin.center_x = player_file.Player.sprite.center_x

        # if coin count is greater than COINS_AFTER_PARTY and the player is moving slowly, then deactivate party
        if (Coin.score > COINS_AFTER_PARTY) and (
            abs(player_file.Player.sprite.velocity_y) < 5
        ):
            # reset coin count
            Coin.score = 0

            # change stuff to their non-party counterparts
            gameview_file.GameView.party = False
            gameview_file.GameView.time_factor_change = (
                my_constants.TIME_FACTOR_CHANGE_MANAGER["not_party"]
            )
            gameview_file.GameView.time_factor = (
                gameview_file.GameView.time_factor_not_party
            )


def setup():
    """Set up the game and initialize the variables."""
    Coin.list = arcade.SpriteList()
    Coin.score = 0
    gameview_file.GameView.party = False


my_constants.coin["Input_class"] = Coin
