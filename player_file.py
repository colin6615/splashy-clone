"""holds player class, setup() and update()"""

import arcade

import gameview_file
import my_constants


class Player(arcade.Sprite):
    """Creates player and handles free-fall physics

    Attributes:
        input_path (str): Description of the attribute
        sprite (Sprite): sprite
            Sub-Attributes:
                velocity (float): velocity in y-direction
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
    Player.sprite.velocity = 0

    # make list and add sprite to list
    Player.list = arcade.SpriteList()
    Player.list.append(Player.sprite)


def update():
    """Movement and game logic"""

    # free-fall physics in the y-direciton
    # must update acceleration every tick because acceleration changes with velocity.
    # define acceleration: a = T * (- g + b * |v|)
    Player.sprite.acceleration = gameview_file.GameView.time_factor * (
        -my_constants.GRAVITATIONAL_ACCELERATION
        + my_constants.DRAG_COEFFICIENT * abs(Player.sprite.velocity)
    )

    # calculate position and velocity using kinematics
    if gameview_file.GameView.started == True:
        Player.sprite.velocity += Player.sprite.acceleration
        Player.sprite.center_y += Player.sprite.velocity
