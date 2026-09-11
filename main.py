"""start the game

Creates an instance of the window class, which shows up on screen.
"""

import arcade

import gameview_file

WINDOW_TITLE = "Splashy Clone"


def main():

    # make instance of window class
    window = arcade.Window(950, 550, WINDOW_TITLE, fullscreen=False)

    # start the gameplay
    gameview = gameview_file.GameView()
    gameview.setup()

    # put gameplay in the window instance
    window.show_view(gameview)
    arcade.run()


if __name__ == "__main__":
    main()
