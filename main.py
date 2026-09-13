"""start the games"""

import arcade

import gameview_file

WINDOW_TITLE = "Splashy Clone"


def main():
    """creates a window and starts the game"""
    window = arcade.Window(950, 550, WINDOW_TITLE, fullscreen=False)

    # start the gameplay
    gameview = gameview_file.GameView()
    gameview.setup()

    # show gameplay in the window
    window.show_view(gameview)

    arcade.run()


if __name__ == "__main__":
    main()
