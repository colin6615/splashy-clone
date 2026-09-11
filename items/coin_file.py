"""This file holds the Coin class and setup() function.

This file also adds the "input class" key to the coin dictionary.

Coins are items that the player can interact with.
"""

from threading import Timer

import arcade

import gameview_file
import items.item_file
import items.pad_file
import items.spike_file
import items.target_file
import my_constants
import player_file


# ================================
# Party functions
# ===============================
# during a coin party, coin sounds play constantly. I don't want multiple coin sounds to play at once, so I created this function.
# note that I don't use this sort of function for other sounds because other sounds don't play constantly.
def coin_sound():
    """play coins sound if coin sound is not already playing"""
    if not Coin.coin_sound_player or not Coin.coin_sound_player.playing:
        Coin.coin_sound_player = arcade.play_sound(my_constants.coin["sound"])


def party_finish_true():
    Coin.party_finish = True


class Coin(items.item_file.Item):
    """
    handles coin collection and parties

    Class Attributes:
        list (SpriteList): list of all coin sprites
        collected_count (float): how many coins were collected by the player
    """

    def setup():
        """Set up the game and initialize the variables."""
        Coin.party_finish = False
        Coin.coin_sound_player = None
        # values at start of game
        Coin.list = arcade.SpriteList()
        Coin.collected_count = 0

        # non-party values
        gameview_file.GameView.party = False
        gameview_file.GameView.game_speed_factor = 1

    def update(self, delta_time):
        """Triggers coin party or collects coins, if needed.
        Args:
            delta_time (int): framerate in hertz. how many times per second that the game updates.

        During a coin party, the player can't die, and game speed increases
        If the player hits a coin, then increase the score multiplier and delete the coin"""

        # next 3 loc: if player hits coin, then for each colliding coin:
        colliding_player_and_coin = arcade.check_for_collision_with_list(
            player_file.Player.sprite, Coin.list
        )
        for colliding_sprite in colliding_player_and_coin:
            if colliding_sprite in Coin.list:
                # remove coin from sprite list
                # reason: ensures that player interacts with each coin once
                colliding_sprite.remove_from_sprite_lists()

                coin_sound()
                Coin.collected_count += 1

        # if the coin count is greater than the coin party count, then:
        # this "if" statement is only true, at the start of a party, for one update-tick.
        if my_constants.coin["party_count"] <= Coin.collected_count:
            # activate party mode
            gameview_file.GameView.party = True

            # increase game speed
            gameview_file.GameView.game_speed_factor = (
                my_constants.game_speed_factor_party
            )

            # reset coin count
            Coin.collected_count = 0

            # finish the party after a while.
            # set party_finish to true after the party duration, seconds_per_party
            #   Source - https://stackoverflow.com/a/44666336
            #   Posted by Aaron Hall, modified by community. See post 'Timeline' for change history
            #   Retrieved 2026-09-10, License - CC BY-SA 4.0
            # create the timer, which runs party_finish_true() after "seconds_per_party" seconds have passed.
            party_deactivation_timer = Timer(
                my_constants.coin["seconds_per_party"], party_finish_true
            )
            # start the timer
            party_deactivation_timer.start()

        # this code runs once per tick, during a party
        if gameview_file.GameView.party == True:
            # play coin sound
            coin_sound()

            # remove spikes, so that the player doesn't die
            for spike in items.spike_file.Spike.list:
                spike.remove_from_sprite_lists()

            # move the pads, targets, and coins to the player
            for sprite_list in [
                items.pad_file.Pad.list,
                items.target_file.Target.list,
                Coin.list,
            ]:
                for item in sprite_list:
                    item.center_x = player_file.Player.sprite.center_x

        # if coin count is greater than COINS_AFTER_PARTY and the player is moving slowly, then deactivate party
        player_move_slow = abs(player_file.Player.sprite.velocity_y) < 2.5
        if Coin.party_finish == True and player_move_slow == True:
            gameview_file.GameView.party = False
            Coin.party_finish = False

            # reset game speed
            gameview_file.GameView.game_speed_factor = 1


my_constants.coin["Input_class"] = Coin
