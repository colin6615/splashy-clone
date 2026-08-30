"""
Scroll around a large screen.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_scrolling_pad
"""

import arcade

import gameview_file
import my_constants

WINDOW_TITLE = "Splashy Clone"


class Testy:
    window = arcade.Window(
        my_constants.WINDOW_WIDTH, my_constants.WINDOW_HEIGHT, WINDOW_TITLE
    )

    def main():
        # Create a window class. This is what actually shows up on screen

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        # window.set_mouse_visible(False)

        # Begin with StarView
        gameview = gameview_file.GameView()
        gameview.setup()

        Testy.window.show_view(gameview)

        arcade.run()

    def game_over_function():
        game_over_view = gameover_file.GameOverView()
        Testy.window.show_view(game_over_view)


import gameover_file

if __name__ == "__main__":
    Testy.main()
