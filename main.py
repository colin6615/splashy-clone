"""start the game

Creates an instance of the window class, which shows up on screen.
"""

import arcade

import gameview_file
import my_constants

WINDOW_TITLE = "Splashy Clone"
window = arcade.Window(
    my_constants.WINDOW_WIDTH,
    my_constants.WINDOW_HEIGHT,
    WINDOW_TITLE,
    fullscreen=True,
)


def main():
    # make instance of window class

    # start the gameplay
    gameview = gameview_file.GameView()
    gameview.setup()

    # put gameplay in the window instance
    window.show_view(gameview)
    arcade.run()


if __name__ == "__main__":
    main()
