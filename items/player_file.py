"""holds player class, which has setup(), update(), update_acceleration_factor(). Outside of the class, there is asymptotic_function()"""

import arcade

import gameview_file
import items.item_file
import my_constants


def asymptotic_function(x, max_y, x_at_half_y):
    """
    inputs 3 numbers and outputs 1 number.

    Args:
        x (float): input variable
        max_y (float): maximum output
            reached at infinity
            asymptotic_function(x = infinity) = max_y
        x_at_half_y (float): At this x value, output is  (sort of) halfway maxed out.
            asymptotic_function(x = x_at_half_y) = [(max_y - 1) / 2] + 1
    Returns:
        output (float)
    """

    numerator = (max_y - 1) * x
    denominator = x + x_at_half_y
    y = 1 + numerator / denominator
    return y


class Player(items.item_file.Item):
    """Creates player and handles free-fall physics

    Class Attributes:
        sprite (Sprite): sprite
            Sub-Attributes:
                velocity_y (float): velocity in y-direction
                center_y (float): y-position of center
                center_x (float): x-position of center
                position (tuple): (center_x, center_y)
        list (SpriteList): holds the sprite.
        gravity_factor (float): controls gravity strength.
            * 1 = gravity is normal
            * 3 = gravity is 3 times stronger
            * value is my_constants.gravity_factor_party if party is true. Else: 1
        bounce_count (float): Total number of times that the player has bounced.
    """

    def update_acceleration_factor():
        """updates Player.acceleration_factor speed up the game over time

        This is super jank. Future-me please find a better way to update this variable.
        """
        Player.acceleration_factor = asymptotic_function(
            x=Player.bounce_count, max_y=2.5, x_at_half_y=36
        )

    def setup():
        """Make the sprite and add it to its sprite list"""
        Player.sprite = items.item_file.spawn(
            x_input=256, y_input=0, **my_constants.player
        )
        Player.sprite.velocity_y = 0
        Player.list = arcade.SpriteList()
        Player.list.append(Player.sprite)
        Player.update_acceleration_factor()

    def update():
        """Handles free-fall physics"""

        # free-fall physics in the y-direciton
        # must update acceleration every tick because acceleration changes with velocity_y.
        # define acceleration
        v = Player.sprite.velocity_y
        g = my_constants.GRAVITATIONAL_ACCELERATION
        b = my_constants.DRAG_COEFFICIENT
        af = Player.acceleration_factor

        # scales gravity. Has 2 values: one value during party and another value during non-party.
        gf = Player.gravity_factor

        Player.sprite.acceleration = (-g * gf + b * abs(v)) * af

        # calculate position and velocity_y using kinematics
        if gameview_file.GameView.started == True:
            Player.sprite.velocity_y += Player.sprite.acceleration
            Player.sprite.center_y += Player.sprite.velocity_y


my_constants.player["Input_class"] = Player
