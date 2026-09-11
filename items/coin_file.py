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

# party duration in seconds
SECONDS_PER_PARTY = 6.5


# ================================
# Party functions
# ===============================
# during a coin party, coin sounds play constantly. I don't want multiple coin sounds to play at once, so I created this function.
# note that I don't use this sort of function for other sounds because other sounds don't play constantly.
def coin_sound():
    """play coins sound if coin sound is not already playing. Only 1 coin sound can play at a time."""
    if not Coin.coin_sound_player or not Coin.coin_sound_player.playing:
        Coin.coin_sound_player = arcade.play_sound(my_constants.coin["sound"])


def party_finish_true():
    """sets a bool to True"""
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
        Coin.list = arcade.SpriteList()
        Coin.collected_count = 0
        gameview_file.GameView.party = False
        gameview_file.GameView.game_speed_factor = 1
        Coin.coin_sound_player = None

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
                # remove coin from sprite list to make sure that player interacts with coin once
                colliding_sprite.remove_from_sprite_lists()

                coin_sound()

                # increase coin count
                Coin.collected_count += 1

        # if the coin count is too high, then activate a party.
        # this "if" statement is true one tick per party.
        #   true at the start of the party
        #   false during a party. false without a party.
        if my_constants.coin["max"] <= Coin.collected_count:
            # activate party mode
            gameview_file.GameView.party = True

            # increase game speed
            gameview_file.GameView.game_speed_factor = (
                my_constants.game_speed_factor_party
            )

            # reset coin count
            Coin.collected_count = 0

            # deactivate party mode after a while
            #   Source - https://stackoverflow.com/a/44666336
            #   Posted by Aaron Hall, modified by community. See post 'Timeline' for change history
            #   Retrieved 2026-09-10, License - CC BY-SA 4.0
            party_deactivation_timer = Timer(SECONDS_PER_PARTY, party_finish_true)
            # later: can i remove args=None, kwargs=None? can move this above
            party_deactivation_timer.start()

        # if party mode is activated, then run this code once per tick
        # this code runs continously during a party.
        if gameview_file.GameView.party == True:
            coin_sound()

            # remove spikes, so that the player doesn't die
            for spike in items.spike_file.Spike.list:
                spike.remove_from_sprite_lists()

            # move the pads, targets, and coins to the player
            for item in (
                items.pad_file.Pad.list,
                items.target_file.Target.list,
                Coin.list,
            ):
                item.center_x = player_file.Player.sprite.center_x
            for item in items.pad_file.Pad.list:
                item.center_x = player_file.Player.sprite.center_x

        # if coin count is greater than COINS_AFTER_PARTY and the player is moving slowly, then deactivate party
        player_move_slow = abs(player_file.Player.sprite.velocity_y) < 2.5
        if Coin.party_finish == True and player_move_slow == True:
            gameview_file.GameView.party = False
            Coin.party_finish = False

            # reset game speed
            gameview_file.GameView.game_speed_factor = 1


my_constants.coin["Input_class"] = Coin
