import arcade

import gameview_file
import my_constants


class StartView(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.WHITE

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Start Screen",
            my_constants.WINDOW_WIDTH / 2,
            my_constants.WINDOW_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "Click to advance",
            my_constants.WINDOW_WIDTH / 2,
            my_constants.WINDOW_HEIGHT / 2 - 75,
            arcade.color.GRAY,
            font_size=20,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        gameview = gameview_file.GameView()
        gameview.setup()
        self.window.show_view(gameview)
