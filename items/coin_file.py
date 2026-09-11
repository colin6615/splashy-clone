"""This file holds the Coin class and setup() function.

This file also adds the "input class" key to the coin dictionary.

Coins are items that the player can interact with.
"""

import arcade

import gameview_file
import items.item_file
import items.pad_file
import items.spike_file
import items.target_file
import my_constants
import player_file

# a coin party happens every several coins that the player collects. During a coin party, the user cannot die.
# in the next 2 sections, I will calculate how many coins are added to the coin count during the party
# ================================
# coin party constants
# ================================
# how many coins are added to the coin count every update during party
COINS_PER_UPDATE = 0.1

# empirical value (i think its constant, but idk.)
UPDATES_PER_SECOND = 250

# party duration in seconds
SECONDS_PER_PARTY = 6.5
# ================================
# coin party calculations
# ================================
#  how many coins are added to the coin count during the party
COIN_CHANGE_PER_PARTY = UPDATES_PER_SECOND * SECONDS_PER_PARTY * COINS_PER_UPDATE

# the maximum number of coins during a party. The coin count at the end of the party
COINS_AFTER_PARTY = my_constants.coin["max"] + COIN_CHANGE_PER_PARTY


# ================================
def coin_sound():
    if not Coin.coin_sound_player or not Coin.coin_sound_player.playing:
        Coin.coin_sound_player = arcade.play_sound(my_constants.coin["sound"])


class Coin(items.item_file.Item):
    """
    handles coin collection and parties

    Class Attributes:
        list (SpriteList): list of all coin sprites
        collected_count (float): how many coins were collected by the player
    """

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

                # play coin sound
                # only 1 coin sound can play at a time. Don't play coin sound if coin sound is already playing
                coin_sound()
                # increase coin count
                Coin.collected_count += 1
        # if the coin count is in the party range, then:
        if my_constants.coin["max"] <= Coin.collected_count < COINS_AFTER_PARTY:
            # change stuff to their party counterparts
            gameview_file.GameView.party = True
            gameview_file.GameView.game_speed_factor = (
                my_constants.game_speed_factor_party
            )

            # increase coin count
            Coin.collected_count += COINS_PER_UPDATE

            # play coin sound. same deal as before, where only 1 coin sound can play at once.
            coin_sound()

            # remove spikes, so that the player doesn't die
            for spike in items.spike_file.Spike.list:
                spike.remove_from_sprite_lists()

            # move the pads and target to the player
            for pad in items.pad_file.Pad.list:
                pad.center_x = player_file.Player.sprite.center_x
            for target in items.target_file.Target.list:
                target.center_x = player_file.Player.sprite.center_x
            for coin in Coin.list:
                coin.center_x = player_file.Player.sprite.center_x

        # if coin count is greater than COINS_AFTER_PARTY and the player is moving slowly, then deactivate party
        if (Coin.collected_count > COINS_AFTER_PARTY) and (
            abs(player_file.Player.sprite.velocity_y) < 2.5
        ):
            # reset coin count
            Coin.collected_count = 0

            # change stuff to their non-party counterparts
            gameview_file.GameView.party = False
            gameview_file.GameView.game_speed_factor = 1

    def setup():
        """Set up the game and initialize the variables."""
        Coin.list = arcade.SpriteList()
        Coin.collected_count = 0
        gameview_file.GameView.party = False
        gameview_file.GameView.game_speed_factor = 1
        Coin.coin_sound_player = None


my_constants.coin["Input_class"] = Coin
