"""Game over screen"""

import arcade

import gameview_file
import my_constants


class GameOverView(arcade.View):
    """Displays score and prompts the user to restart the game."""

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        self.window.background_color = arcade.color.GREEN_YELLOW
        # check if the user got a high score.
        # The "with" block was sourced from
        # https://stackoverflow.com/a/47422975
        # Posted by TemporalWolf, modified by community. See post 'Timeline' for change history
        # Retrieved 2026-08-30, License - CC BY-SA 3.0
        with open("highscore.txt", "r+") as hisc:
            hi = hisc.read()
            if not hi:  # not hi will only be true for strings on an empty string
                hi = "0"
            if gameview_file.GameView.score > int(hi):
                self.high_score_variable = gameview_file.GameView.score
                hisc.seek(
                    0
                )  # We already read to the end. We need to go back to the start
                hisc.write(str(gameview_file.GameView.score))
                hisc.truncate()  # Delete anything left over... not strictly necessary
            else:
                self.high_score_variable = hi

    def on_draw(self):
        self.clear()
        """
        Draws text in a 1x4 array
        """
        # set y-postion of the top text
        text_y = int(self.height * 0.75)

        # write text
        previous_score_text = f"Previous Score: {gameview_file.GameView.score}"
        high_score_text = f"High Score: {self.high_score_variable}"

        # create dictionaries to loop over. These dictionaries contain the text font and content
        game_over = {"text": "Game Over", "font_size": 54}
        instruction = {"text": my_constants.instruction_text, "font_size": 24}
        previous_score = {"text": previous_score_text, "font_size": 24}
        high_score = {"text": high_score_text, "font_size": 24}
        text_dicts = [game_over, instruction, previous_score, high_score]

        # draw the text from the dictionaries
        for dict in text_dicts:
            arcade.Text(
                dict["text"],
                x=int(self.width / 2),
                y=text_y,
                color=arcade.color.WHITE,
                font_size=dict["font_size"],
                anchor_x="center",
            ).draw()

            # make each text box lower than the last. This way, the text boxes don't overlap each other
            text_y -= 100

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Restart the game upon click"""
        game_view = gameview_file.GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        """if user presses escape, then close the window"""
        if key == arcade.key.ESCAPE:
            arcade.close_window()
