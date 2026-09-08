"""handles gameplay"""

import time

import arcade

import camera_file
import gameover_file
import items.coin_file
import items.pad_file
import items.spike_file
import items.target_file
import main
import my_constants
import player_file

# ==================
# time_factor_change speeds up the game after every bounce.
# NOTE: 0 = no speed change
# NOTE: starting time_factor is 1, so after the n-th bounce, it updates to time_factor + TIME_FACTOR_CHANGE * N


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
        width, height = main.window.get_size()
        print(width)

        # Reset numbers to their starting values.
        GameView.score = 0
        GameView.score_factor = 1

        # other initial values
        GameView.started = False
        GameView.dead = False

        camera_file.my_camera.setup(self)

        # create SpriteLists and initial values for sprites
        items.target_file.Target.setup()
        items.coin_file.Coin.setup()
        items.spike_file.Spike.setup()
        player_file.Player.setup()
        # spawn the first 4 pads
        items.pad_file.Pad.setup()

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

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw sprites.
        player_file.Player.list.draw()
        items.pad_file.Pad.list.draw()
        items.target_file.Target.list.draw()
        items.coin_file.Coin.list.draw()
        items.spike_file.Spike.list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Draw the coin score
        coin_count = str(items.coin_file.Coin.score)
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
                my_constants.instruction_text,
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
        arcade.play_sound(my_constants.death_sound)
        time.sleep(my_constants.SLEEP_AFTER_DEAD)

        # switch the window to game over screen
        self.window.show_view(game_over_view)

    def on_update(self, delta_time):
        """Movement and game logic. This function calls every game tick"""
        # update sprites .
        player_file.Player.update()
        items.pad_file.Pad.list.update()
        items.target_file.Target.list.update()
        items.coin_file.Coin.list.update()
        items.spike_file.Spike.list.update()

        # Scroll the screen to the player
        camera_file.my_camera.scroll_to_player(self)

        # if player is dead, then go to game end screen
        if GameView.dead == True:
            GameView.game_over_function(self)

    def on_key_press(self, key, modifiers):
        """if user presses escape, then close the window"""
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_resize(self, width: int, height: int):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        super().on_resize(width, height)
        self.camera_sprites.match_window()
        self.camera_gui.match_window(position=True)
