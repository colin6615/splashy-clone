"""
Scroll around a large screen.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_scrolling_pad
"""

import arcade

import gameview_file
import my_constants

WINDOW_TITLE = "Sprite Move with Scrolling Screen Example"


def main():
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(
        my_constants.WINDOW_WIDTH, my_constants.WINDOW_HEIGHT, WINDOW_TITLE
    )

    # Make the mouse disappear when it is over the window.
    # So we just see our object, not the pointer.
    window.set_mouse_visible(False)

    # Create and setup the GameView
    game = gameview_file.GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
