"""handles gameplay"""

import random

import arcade

import gameover_file
import my_constants
import pad_file
import player_file
import target_file

# -- Constants
# If the player moves further than this boundary away from the camera we use a
# constraint to move the camera
HORIZONTAL_BOUNDARY = my_constants.WINDOW_WIDTH / 2.0
BOTTOM_BOUNDARY = 0
TOP_BOUNDARY = my_constants.WINDOW_HEIGHT / 2.0 - 100

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.6
# ==================


CAMERA_BOUNDARY = arcade.LRBT(
    -HORIZONTAL_BOUNDARY,
    HORIZONTAL_BOUNDARY,
    -BOTTOM_BOUNDARY,
    TOP_BOUNDARY,
)


class GameView(arcade.View):
    """
    If the player isn't dead, and the game has already started, then this file runs. The user can have 'fun' playing the game.

    Class Attributes:
        score (int): player's current score.
        score_factor (int): How many points are added to the score after a bounce.
            example: If score_factor=2, and 1 bounce happens, then score increases by 2.
        time_factor (float): bounce speed
        started (bool): Has the game started?
        dead (bool): Is the player dead?
    """

    def setup(self):
        """Set up the game and initialize the variables."""
        # Sprite lists
        self.coin_list = None

        # Reset numbers to their starting values.
        GameView.score = 0
        GameView.score_factor = 1
        GameView.time_factor = 1
        GameView.started = False
        GameView.dead = False

        # camera stuff
        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

        # spawn player and 2 pads.
        self.coin_list = arcade.SpriteList()
        target_file.setup()
        pad_file.Pad.setup()

        player_file.setup()

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

        self.background_color = arcade.color.AMAZON

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Start the game when the user clicks
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            GameView.started = True

    def on_mouse_motion(self, x, y, dx, dy):
        """move the player's x-position with mouse"""
        player_file.Player.sprite.center_x = x

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        player_file.Player.list.draw()
        pad_file.Pad.list.draw()
        target_file.Target.list.draw()
        self.coin_list.draw()

        # Draw the pad that we work to make sure the user stays inside of.
        # This is just for illustration purposes.
        # remove upon release
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
        score_text = str(GameView.score)
        arcade.draw_text(score_text, 10, 10, arcade.color.BLACK_BEAN, 20)

        # Instruct the user to start the game by clicking, if they haven't started the game yet.
        if GameView.started == False:
            arcade.draw_text(
                "Left click to start",
                x=my_constants.WINDOW_WIDTH / 2,
                y=my_constants.WINDOW_WIDTH / 4,
                color=arcade.color.WHITE,
                font_size=24,
                anchor_x="center",
            )

    def game_over_function(self):
        """Stop gameplay. Switch to game over screen."""
        # create game over screen
        game_over_view = gameover_file.GameOverView()

        # show the mouse
        self.window.set_mouse_visible(True)
        # switch the window to game over screen
        self.window.show_view(game_over_view)

    def on_update(self, delta_time):
        """Movement and game logic. This function calls every game tick"""
        # update pads and player.
        pad_file.Pad.list.update()
        player_file.update()
        target_file.Target.list.update()

        # Scroll the screen to the player
        self.scroll_to_player()

        # if player is dead, then go to game end screen
        if GameView.dead == True:
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
            player_file.Player.sprite.position,
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
