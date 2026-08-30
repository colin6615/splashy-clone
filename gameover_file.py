import arcade

import gameview_file
import my_constants


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        self.window.background_color = arcade.color.GREEN_YELLOW

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

        output_total = f"Total Score: {gameview_file.GameView.score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = gameview_file.GameView()
        self.window.show_view(game_view)
