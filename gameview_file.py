"""handles gameplay"""

import time

import arcade

import coin_file
import gameover_file
import my_constants
import pad_file
import player_file
import spike_file
import target_file

CAMERA_BOUNDARY = arcade.LRBT(
    -my_constants.HORIZONTAL_BOUNDARY,
    my_constants.HORIZONTAL_BOUNDARY,
    -my_constants.BOTTOM_BOUNDARY,
    my_constants.TOP_BOUNDARY,
)


class GameView(arcade.View):
    """
    If the player isn't dead, and the game has already started, then this file runs. The user can have 'fun' playing the game.

    Class Attributes:
        score (int): player's current score.
        score_factor (int): How many points are added to the score after a bounce.
            example: If score_factor=2, and 1 bounce happens, then score increases by 2.
        started (bool): Has the game started?
        dead (bool): Is the player dead?
    """

    def setup(self):
        """Set up the game and initialize the variables."""

        # Reset numbers to their starting values.
        GameView.score = 0
        GameView.score_factor = 1

        # I should use a state machine for this.
        # this value is high during a party. 1 otherwise
        GameView.hype = 1

        # other initial values
        GameView.started = False
        GameView.dead = False

        # camera stuff
        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

        # create SpriteLists and initial values for sprites
        target_file.setup()
        coin_file.setup()
        spike_file.setup()
        player_file.setup()
        # spawn the first 4 pads
        pad_file.Pad.setup()

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

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Draw the score
        score_text = str(GameView.score)
        str(GameView.score)
        arcade.draw_text(
            score_text,
            my_constants.WINDOW_WIDTH / 2,
            my_constants.WINDOW_HEIGHT - 40,
            arcade.color.BLACK_BEAN,
            font_size=35,
            anchor_x="center",
        )

        # Draw the score factor
        score_factor_text = f"X {GameView.score_factor}"
        arcade.draw_text(
            score_factor_text,
            my_constants.WINDOW_WIDTH / 2,
            my_constants.WINDOW_HEIGHT * 0.4,
            arcade.color.WHITE,
            font_size=35,
            anchor_x="center",
        )

        # Draw the coin score
        coin_count = str(coin_file.Coin.score)
        arcade.draw_text(
            "Coins: " + coin_count,
            my_constants.WINDOW_WIDTH - 150,
            30,
            arcade.color.GOLD,
            font_size=25,
        )

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

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw sprites.
        player_file.Player.list.draw()
        pad_file.Pad.list.draw()
        target_file.Target.list.draw()
        coin_file.Coin.list.draw()
        spike_file.Spike.list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

    def game_over_function(self):
        """Stop gameplay. Switch to game over screen."""
        # create game over screen
        game_over_view = gameover_file.GameOverView()

        # show the mouse
        self.window.set_mouse_visible(True)

        time.sleep(my_constants.SLEEP_AFTER_DEAD)

        # switch the window to game over screen
        self.window.show_view(game_over_view)

    def on_update(self, delta_time):
        """Movement and game logic. This function calls every game tick"""
        # update sprites .
        pad_file.Pad.list.update()
        player_file.update()
        target_file.Target.list.update()
        coin_file.Coin.list.update()
        spike_file.Spike.list.update()

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
            my_constants.CAMERA_SPEED,
        )
