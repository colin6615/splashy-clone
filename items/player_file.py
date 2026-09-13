"""holds player class, setup() and update()"""

import arcade

import gameview_file
import items.item_file
import my_constants


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
    """

    def setup():
        """Make the sprite and add it to its sprite list"""
        Player.sprite = items.item_file.spawn(
            x_input=256, y_input=0, **my_constants.player
        )
        Player.sprite.velocity_y = 0
        Player.list = arcade.SpriteList()
        Player.list.append(Player.sprite)

    def update():
        """Handles free-fall physics"""

        # free-fall physics in the y-direciton
        # must update acceleration every tick because acceleration changes with velocity_y.
        # define acceleration
        v = Player.sprite.velocity_y
        g = my_constants.GRAVITATIONAL_ACCELERATION
        b = my_constants.DRAG_COEFFICIENT

        # speeds up the game over time
        game_speed = gameview_file.GameView.game_speed_function

        # scales gravity. Has 2 values: one value during party and another value during non-party.
        gf = gameview_file.GameView.gravity_factor

        Player.sprite.acceleration = (-g * gf + b * abs(v)) * game_speed

        # calculate position and velocity_y using kinematics
        if gameview_file.GameView.started == True:
            Player.sprite.velocity_y += Player.sprite.acceleration
            Player.sprite.center_y += Player.sprite.velocity_y


my_constants.player["Input_class"] = Player
