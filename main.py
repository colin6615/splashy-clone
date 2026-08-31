"""
run gameview to start the game

Attributes:
None (I think?)

.
"""

import arcade

import gameview_file
import my_constants

WINDOW_TITLE = "Splashy Clone"


def main():
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(
        my_constants.WINDOW_WIDTH, my_constants.WINDOW_HEIGHT, WINDOW_TITLE
    )

    # create and run Gameview
    gameview = gameview_file.GameView()
    gameview.setup()
    window.show_view(gameview)
    arcade.run()


if __name__ == "__main__":
    main()
