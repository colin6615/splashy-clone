"""holds player class, setup() and update()"""

import arcade

import gameview_file
import my_constants
import pad_file


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


class Player(arcade.Sprite):
    """Creates player and handles free-fall physics

    Attributes:
        input_path (str): Description of the attribute
        sprite (Sprite): sprite
            Sub-Attributes:
                velocity_y (float): velocity in y-direction
                center_y (float): y-position of center
        list (SpriteList): holds the sprite.
    """

    def __init__(self, filename, sprite_scaling):
        """Call the parent class (Sprite) constructor"""
        super().__init__(filename, sprite_scaling)


def setup():
    """Make the sprite and list"""
    Player.sprite = arcade.Sprite(
        ":resources:images/animated_characters/female_person/femalePerson_idle.png",
        scale=0.4,
    )

    # set the sprite's starting values
    Player.sprite.center_x = 256
    Player.sprite.center_y = 0
    Player.sprite.velocity_y = 0

    # make list and add sprite to list
    Player.list = arcade.SpriteList()
    Player.list.append(Player.sprite)


def update():
    """Movement and game logic"""

    # free-fall physics in the y-direciton
    # must update acceleration every tick because acceleration changes with velocity_y.
    # define acceleration: a = tau * (- g + b * |v|)
    # speeds up the game over time
    Player.game_speed = gameview_file.GameView.hype * asymptotic_function(
        pad_file.Pad.total, 6, 80
    )
    tau = Player.game_speed
    v = Player.sprite.velocity_y
    g = my_constants.GRAVITATIONAL_ACCELERATION
    b = my_constants.DRAG_COEFFICIENT

    Player.sprite.acceleration = tau * (-g + b * abs(v))

    # calculate position and velocity_y using kinematics
    if gameview_file.GameView.started == True:
        Player.sprite.velocity_y += Player.sprite.acceleration
        Player.sprite.center_y += Player.sprite.velocity_y
