"""
Scroll around a large screen.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_scrolling_pad
"""

import random

import arcade
import numpy as np

import my_constants
import my_platform

SPRITE_SCALING = 0.5

SPRITE_SCALING_COIN = 0.3

NUMBER_OF_COINS = 50

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Sprite Move with Scrolling Screen Example"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200
HORIZONTAL_BOUNDARY = WINDOW_WIDTH / 2.0 - VIEWPORT_MARGIN
VERTICAL_BOUNDARY = WINDOW_HEIGHT / 2.0 - VIEWPORT_MARGIN
# If the player moves further than this boundary away from the camera we use a
# constraint to move the camera
CAMERA_BOUNDARY = arcade.LRBT(
    -HORIZONTAL_BOUNDARY,
    HORIZONTAL_BOUNDARY,
    -VERTICAL_BOUNDARY,
    VERTICAL_BOUNDARY,
)

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.2


class GameView(arcade.View):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        # Sprite lists
        self.player_list = None
        my_platform.Pad.list = None
        self.coin_list = None

        my_platform.Pad.y_values_list = None

        # Set up the player
        self.player_sprite = None

        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

    def setup(self):
        """Set up the game and initialize the variables."""

        # Sprite lists
        self.player_list = arcade.SpriteList()
        my_platform.Pad.list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        my_platform.Pad.y_values_list = []

        # Set up the player
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            scale=0.4,
        )
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)

        self.player_sprite.velocity = 0

        # define acceleration: a = - g + b * |v|
        self.player_sprite.acceleration = (
            -my_constants.GRAVITATIONAL_ACCELERATION
            + my_constants.DRAG_COEFFICIENT * abs(self.player_sprite.velocity)
        )

        # Place pads inside a loop. 4 sets of 3 pads.
        for y in range(
            -my_constants.DELTA_Y, my_constants.DELTA_Y, my_constants.DELTA_Y
        ):
            my_platform.Pad.spawn_pad(x_input=4, y_input=y)

        # Create the coins
        for i in range(NUMBER_OF_COINS):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(
                ":resources:images/items/coinGold.png",
                scale=SPRITE_SCALING_COIN,
            )
            # Position the coin.
            coin.center_x = random.randrange(10, 1000)
            coin.center_y = random.randrange(10, 1000)

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Set the background color
        self.background_color = arcade.color.AMAZON

    def on_mouse_motion(self, x, y, dx, dy):
        """Called to update our objects.
        Happens approximately 60 times per second."""
        self.player_sprite.center_x = x

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.

        self.player_list.draw()
        my_platform.Pad.list.draw()
        self.coin_list.draw()

        # Draw the pad that we work to make sure the user stays inside of.
        # This is just for illustration purposes. You'd want to remove this
        # in your game.
        camera_x, camera_y = self.camera_sprites.position
        arcade.draw_rect_outline(
            arcade.XYWH(
                camera_x, camera_y, CAMERA_BOUNDARY.width, CAMERA_BOUNDARY.height
            ),
            arcade.color.RED,
            2,
        )

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Draw the GUI
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.width // 2, 20, self.width, 40),
            color=arcade.color.ALMOND,
        )
        text = (
            f"Scroll value: ({self.camera_sprites.position[0]:5.1f}",
            f"{self.camera_sprites.position[1]:5.1f})",
        )
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Calculate speed based on the keys pressed
        self.player_sprite.velocity += self.player_sprite.acceleration
        self.player_sprite.center_y += self.player_sprite.velocity

        # Scroll the screen to the player
        self.scroll_to_player()
        my_platform.Pad.list.update(delta_time)

        pad_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, my_platform.Pad.list
        )

        for pad2 in pad_hit_list:
            # teleport the hit pad below the lowest current pad to make it the newest lowest pad
            my_platform.Pad.y_values_list = np.array(
                [pad.center_y for pad in my_platform.Pad.list]
            )

            pad2.center_y = (
                min(my_platform.Pad.y_values_list)
                - my_constants.DELTA_Y * my_constants.PAD_LENGTH
            )
            # Source of next loc.- https://stackoverflow.com/a/57824234
            # Posted by Energya
            # Retrieved 2026-08-28, License - CC BY-SA 4.0
            # there is probably a more efficient way of doing this.
            my_platform.Pad.y_values_list = np.array(
                [pad.center_y for pad in my_platform.Pad.list]
            )
            # bounce
            self.player_sprite.velocity *= -my_constants.BOUNCE_DECAY_CONSTANT

            # lowest pad.center_y in a pad in pad_list
            # generally to get lowest thing in a list, you do min(list)

            # get its y position
            # tp hit pad to that y position

    def scroll_to_player(self):
        """
        Scroll the window to the player.
        This method will attempt to keep the player at least VIEWPORT_MARGIN
        pixels away from the edge.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        # --- Manage Scrolling ---
        new_position = arcade.camera.grips.constrain_boundary_xy(
            self.camera_sprites.view_data, CAMERA_BOUNDARY, self.player_sprite.position
        )

        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position,
            (new_position[0], new_position[1]),
            CAMERA_SPEED,
        )

    def on_resize(self, width: int, height: int):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        super().on_resize(width, height)
        self.camera_sprites.match_window()
        self.camera_gui.match_window(position=True)


def main():
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Make the mouse disappear when it is over the window.
    # So we just see our object, not the pointer.
    window.set_mouse_visible(False)

    # Create and setup the GameView
    game = GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
