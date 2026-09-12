"""holds player class, setup() and update()"""

import arcade

import gameview_file
import items.item_file
import my_constants


class Player(items.item_file.Item):
    """Creates player and handles free-fall physics

    Attributes:
        input_path (str): Description of the attribute
        sprite (Sprite): sprite
            Sub-Attributes:
                velocity_y (float): velocity in y-direction
                center_y (float): y-position of center
        list (SpriteList): holds the sprite.
    """

    def setup():
        """Make the sprite and list"""
        Player.sprite = items.item_file.spawn(
            x_input=256, y_input=0, **my_constants.player
        )

        # set the sprite's starting values
        Player.sprite.velocity_y = 0

        # make list and add sprite to list
        Player.list = arcade.SpriteList()
        Player.list.append(Player.sprite)

    def update():
        """Movement and game logic"""

        # free-fall physics in the y-direciton
        # must update acceleration every tick because acceleration changes with velocity_y.
        # define acceleration
        v = Player.sprite.velocity_y
        g = my_constants.GRAVITATIONAL_ACCELERATION
        b = my_constants.DRAG_COEFFICIENT

        # speeds up the game over time
        game_speed = gameview_file.GameView.game_speed_function

        # scales gravity
        gf = gameview_file.GameView.gravity_factor

        Player.sprite.acceleration = (-g * gf + b * abs(v)) * game_speed

        # calculate position and velocity_y using kinematics
        if gameview_file.GameView.started == True:
            Player.sprite.velocity_y += Player.sprite.acceleration
            Player.sprite.center_y += Player.sprite.velocity_y


my_constants.player["Input_class"] = Player
