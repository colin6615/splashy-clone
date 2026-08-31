import arcade

import gameview_file
import main
import my_constants


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        main.Main.window.background_color = arcade.color.GREEN_YELLOW

        # The with block was sourced from https://stackoverflow.com/a/47422975
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
        Draw "Game over" across the screen.
        """

        arcade.draw_text(
            "Game Over",
            x=my_constants.WINDOW_WIDTH / 2,
            y=400,
            color=arcade.color.WHITE,
            font_size=54,
            anchor_x="center",
        )
        arcade.draw_text(
            "Click to restart",
            x=my_constants.WINDOW_WIDTH / 2,
            y=300,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
        )

        arcade.draw_text(
            f"Previous Score: {gameview_file.GameView.score}",
            x=my_constants.WINDOW_WIDTH / 2,
            y=200,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
        )
        arcade.draw_text(
            f"High Score: {self.high_score_variable}",
            x=my_constants.WINDOW_WIDTH / 2,
            y=100,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = gameview_file.GameView()
        game_view.setup()
        main.Main.window.show_view(game_view)
