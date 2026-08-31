"""Module summary phrase. Detailed description of what this module does, what classes/functions it exposes, and any usage examples if applicable.

Short one-line summary of the class's purpose.

A longer description explaining what the class does, its general state, and how it is meant to be used across your program.
Attributes:
input_path (str): Description of the attribute
"""

import random

import arcade

import gameover_file
import my_constants
import pad_file

# -- Constants
# If the player moves further than this boundary away from the camera we use a
# constraint to move the camera
HORIZONTAL_BOUNDARY = my_constants.WINDOW_WIDTH / 2.0
BOTTOM_BOUNDARY = 0 # camera will move if the player moves down past the middle of the screen.
TOP_BOUNDARY = my_constants.WINDOW_HEIGHT / 2.0 - 100 

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.6


CAMERA_BOUNDARY = arcade.LRBT(
    -HORIZONTAL_BOUNDARY,
    HORIZONTAL_BOUNDARY,
    -BOTTOM_BOUNDARY,
    TOP_BOUNDARY,
)


class GameView(arcade.View):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        # Sprite lists
        GameView.player_list = None
        self.coin_list = None

        # y-level list

        # Set up the player
        GameView.player_sprite = None
        GameView.score = 0
        GameView.score_factor = 1
        GameView.time_factor = 1

        # camera stuff
        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

    def setup(self):
        """Set up the game and initialize the variables."""

        # Sprite lists
        GameView.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        pad_file.Pad.setup()
        # Set up the player
        GameView.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            scale=0.4,
        )
        GameView.player_sprite.center_x = 256
        GameView.player_sprite.center_y = 0
        GameView.player_list.append(GameView.player_sprite)
        GameView.player_sprite.velocity = 0

        # Create the coins
        for i in range(my_constants.NUMBER_OF_COINS):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(
                ":resources:images/items/coinGold.png",
                scale=my_constants.SPRITE_SCALING_COIN,
            )
            # Position the coin.
            coin.center_x = random.randrange(10, 1000)
            coin.center_y = random.randrange(10, 1000)

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Set the background color
        self.background_color = arcade.color.AMAZON

        GameView.started = False
        GameView.player_dead = False

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Start the game when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            GameView.started = True

    def on_mouse_motion(self, x, y, dx, dy):
        """move the player's x-position with mouse"""
        GameView.player_sprite.center_x = x

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        GameView.player_list.draw()
        pad_file.Pad.list.draw()
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

        # Draw the score
        text = str(GameView.score)
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

    def game_over_function(self):
        game_over_view = gameover_file.GameOverView()
        self.window.set_mouse_visible(True)
        self.window.show_view(game_over_view)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # free-fall physics
        # must update acceleration every tick
        # define acceleration: a = T * (- g + b * |v|)
        GameView.player_sprite.acceleration = GameView.time_factor * (
            -my_constants.GRAVITATIONAL_ACCELERATION
            + my_constants.DRAG_COEFFICIENT * abs(GameView.player_sprite.velocity)
        )
        if GameView.started == True:
            GameView.player_sprite.velocity += GameView.player_sprite.acceleration
            GameView.player_sprite.center_y += GameView.player_sprite.velocity

        # Scroll the screen to the player
        self.scroll_to_player()
        pad_file.Pad.update()

        # if a pad is above the player, then end the game.
        # I don't know hwo to move game_over_function() into pad_file.py
        # so, whenever I need to call
        if GameView.player_dead == True:
            GameView.game_over_function(self)

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
            self.camera_sprites.view_data,
            CAMERA_BOUNDARY,
            GameView.player_sprite.position,
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
