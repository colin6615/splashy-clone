import arcade

import gameview_file
import my_constants


class Player(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        """Constructor."""
        # Call the parent class (Sprite) constructor
        super().__init__(filename, sprite_scaling)
        Player.sprite.center_x = 256
        Player.sprite.center_y = 0

    def setup():
        Player.list = None
        Player.sprite = None
        Player.list = arcade.SpriteList()
        Player.sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            scale=0.4,
        )

        Player.sprite.velocity = 0
        Player.list.append(Player.sprite)

    def update():
        """Movement and game logic"""

        # free-fall physics
        # must update acceleration every tick
        # define acceleration: a = T * (- g + b * |v|)
        Player.sprite.acceleration = gameview_file.GameView.time_factor * (
            -my_constants.GRAVITATIONAL_ACCELERATION
            + my_constants.DRAG_COEFFICIENT * abs(Player.sprite.velocity)
        )
        if gameview_file.GameView.started == True:
            Player.sprite.velocity += Player.sprite.acceleration
            Player.sprite.center_y += Player.sprite.velocity
