"""
Scroll around a large screen.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_scrolling_pad
"""

import arcade
import startview_file
import my_constants

WINDOW_TITLE = "hi this is the window. welcome to the window."


def main():
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(
        my_constants.WINDOW_WIDTH, my_constants.WINDOW_HEIGHT, WINDOW_TITLE
    )

    # Make the mouse disappear when it is over the window.
    # So we just see our object, not the pointer.
    window.set_mouse_visible(False)

    # Create and setup the GameView
    start_view = startview_file.StartView()
    window.show_view(start_view)
    arcade.run()





if __name__ == "__main__":
    main()
