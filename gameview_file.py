"""handles gameplay"""

import arcade

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

    # Height and width of the game's internal canvas.
    # DEFAULT ASPECT RATIO = 1.7
    # This aspect ratio is the same for all users.
    # when not in fullscreen, this is the screen resolution
    # WIDTH = height * (DEFAULT ASPECT RATIO)
    internal_width = 1836
    INERNAL_HEIGHT = 1080

    def setup(self):
        """Set up the game and initialize the variables."""

        camera_file.My_camera.setup(self)

        # add sprite width & sound to each dictionary
        # NOTE: includes pad
        for dictionary in [
            my_constants.target,
            my_constants.pad,
            my_constants.coin,
            my_constants.spike,
            my_constants.player,
        ]:
            # load texture from image
            dictionary["image_path"] = f"assets/{dictionary['name']}.png"
            texture = arcade.load_texture(dictionary["image_path"])

            # get width_height tuple
            width_height = texture.size

            # sprite width = image width * image scale
            dictionary["width"] = width_height[0] * dictionary["image_scale"]

        GameView.score = 0
        GameView.score_factor = 1

        # other initial values
        GameView.started = False
        GameView.dead = False

        # create SpriteLists and initial values for sprites
        items.target_file.Target.setup()
        items.coin_file.Coin.setup()
        items.spike_file.Spike.setup()
        items.player_file.Player.setup()
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
        # account for projection of screen (change screen size)
        scaling_factor = GameView.internal_width / camera_file.My_camera.viewport_width

        # move player to mouse
        items.player_file.Player.sprite.center_x = x * scaling_factor

    def on_draw(self):
        """
        Render the screen.
        """
        with self.camera_sprites.activate():
            # This command has to happen before we start drawing
            self.clear()

            # Select the (unscrolled) camera for our GUI
            self.camera_gui.use()

            # Draw the score
            score_text = str(GameView.score)
            str(GameView.score)
            arcade.Text(
                score_text,
                x=GameView.internal_width / 2,
                y=GameView.INERNAL_HEIGHT * 0.92,
                color=arcade.color.BLACK_BEAN,
                font_size=45,
                anchor_x="center",
            ).draw()

            # Draw the score factor
            score_factor_text = f"X {GameView.score_factor}"
            arcade.Text(
                score_factor_text,
                x=GameView.internal_width / 2,
                y=GameView.INERNAL_HEIGHT * 0.42,
                color=arcade.color.WHITE,
                font_size=75,
                anchor_x="center",
            ).draw()

            # Select the camera we'll use to draw all our sprites. The sprites will appear in front of the gui we just drew (in previous loc)
            self.camera_sprites.use()

            # Draw sprites.
            items.player_file.Player.list.draw()
            items.pad_file.Pad.list.draw()
            items.target_file.Target.list.draw()
            items.coin_file.Coin.list.draw()
            items.spike_file.Spike.list.draw()

            # Select the (unscrolled) camera for our GUI. The next gui will appear in the very front; other stuff won't block it.
            self.camera_gui.use()

            # Instruct the user to start the game by clicking, if they haven't started the game yet.
            if GameView.started == False:
                arcade.Text(
                    my_constants.instruction_text,
                    x=GameView.internal_width / 2,
                    y=GameView.INERNAL_HEIGHT * 3 / 4,
                    color=arcade.color.COOL_BLACK,
                    font_size=45,
                    anchor_x="center",
                ).draw()

    def game_over_function(self):
        """Stop gameplay. Switch to game over screen."""
        # create game over screen
        game_over_view = gameover_file.GameOverView()

        # show the mouse
        self.window.set_mouse_visible(True)
        arcade.play_sound(my_constants.death_sound)

        # switch the window to game over screen
        self.window.show_view(game_over_view)

    def on_update(self, delta_time):
        """Movement and game logic. This function calls every game tick
        Args:
            delta_time (int): framerate in hertz. how many times per second that the game updates.
        """
        # update sprites .
        items.player_file.Player.update()
        items.target_file.Target.list.update()
        items.pad_file.Pad.list.update()
        items.coin_file.Coin.list.update()
        items.spike_file.Spike.list.update()

        # Scroll the screen to the player
        camera_file.My_camera.scroll_to_player(self)

        # if player is dead, then go to game end screen
        if GameView.dead == True:
            GameView.game_over_function(self)

    def on_key_press(self, key, modifiers):
        """preform actions using keybinds"""
        # Escape key closes window
        if key == arcade.key.ESCAPE:
            arcade.close_window()

        # F key toggles fullscreen
        camera_file.My_camera._on_key_press(self, key, modifiers)


# circumvent circular import error by placing imports below, rather than above, the class
import camera_file
import gameover_file
import items.coin_file
import items.pad_file
import items.player_file as player_file
import items.spike_file
import items.target_file
import my_constants
