"""
Scroll around a large screen.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_scrolling_box
"""

import random

import arcade

SPRITE_SCALING_BOX = 0.5
SPRITE_SCALING = 0.5
BOX_LENGTH = 64
SPRITE_SCALING_COIN = 0.3


NUMBER_OF_COINS = 50

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Sprite Move with Scrolling Screen Example"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200
HORIZONTAL_BOUNDARY = WINDOW_WIDTH / 2.0 - VIEWPORT_MARGIN
VERTICAL_BOUNDARY = WINDOW_HEIGHT / 2.0 - VIEWPORT_MARGIN
# If the player moves further than this boundary away from the camera we use a
# constraint to move the camera
CAMERA_BOUNDARY = arcade.LRBT(
    -HORIZONTAL_BOUNDARY,
    HORIZONTAL_BOUNDARY,
    -VERTICAL_BOUNDARY,
    VERTICAL_BOUNDARY,
)

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.2

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 7


class GameView(arcade.View):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.coin_list = None

        # Set up the player
        self.player_sprite = None

        self.physics_engine = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

    def setup(self):
        """Set up the game and initialize the variables."""

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            scale=0.4,
        )
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)

        # trap the user in a hollow box. don't let them escape.
        y_min = -8 * BOX_LENGTH
        y_max = 14 * BOX_LENGTH
        x_min = -4 * BOX_LENGTH
        x_max = 15 * BOX_LENGTH

        # Place boxes inside a loop. 4 sets of 3 boxes.
        for y in range(-3, 9, 3):
            for x in range(4, 7, 1):
                wall = arcade.Sprite(
                    ":resources:/images/tiles/boxCrate_double.png", SPRITE_SCALING_BOX
                )
                wall.center_x = x * BOX_LENGTH
                wall.center_y = y * BOX_LENGTH
                self.wall_list.append(wall)

        # -- Randomly place coins where there are no walls
        # Create the coins
        for i in range(NUMBER_OF_COINS):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(
                ":resources:images/items/coinGold.png",
                scale=SPRITE_SCALING_COIN,
            )

            # Boolean variable if we successfully placed the coin
            coin_placed_successfully = False

            # Keep trying until success
            while not coin_placed_successfully:
                # Position the coin.
                HALF_BOX = BOX_LENGTH * 0.5
                x_start = int(x_min + HALF_BOX)
                x_stop = int(x_max - HALF_BOX)
                y_start = int(y_min + HALF_BOX)
                y_stop = int(y_max - HALF_BOX)

                coin.center_x = random.randrange(x_start, x_stop)
                coin.center_y = random.randrange(y_start, y_stop)

                # See if the coin is hitting a wall
                wall_hit_list = arcade.check_for_collision_with_list(
                    coin, self.wall_list
                )

                # See if the coin is hitting another coin
                coin_hit_list = arcade.check_for_collision_with_list(
                    coin, self.coin_list
                )

                if len(wall_hit_list) == 0 and len(coin_hit_list) == 0:
                    # It is!
                    coin_placed_successfully = True

            # Add the coin to the lists
            self.coin_list.append(coin)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list
        )

        # Set the background color
        self.background_color = arcade.color.AMAZON

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()
        self.coin_list.draw()

        # Draw the box that we work to make sure the user stays inside of.
        # This is just for illustration purposes. You'd want to remove this
        # in your game.
        camera_x, camera_y = self.camera_sprites.position
        arcade.draw_rect_outline(
            arcade.XYWH(
                camera_x, camera_y, CAMERA_BOUNDARY.width, CAMERA_BOUNDARY.height
            ),
            arcade.color.RED,
            2,
        )

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Draw the GUI
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.width // 2, 20, self.width, 40),
            color=arcade.color.ALMOND,
        )
        text = (
            f"Scroll value: ({self.camera_sprites.position[0]:5.1f}",
            f"{self.camera_sprites.position[1]:5.1f})",
        )
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Scroll the screen to the player
        self.scroll_to_player()

    def scroll_to_player(self):
        """
        Scroll the window to the player.
        This method will attempt to keep the player at least VIEWPORT_MARGIN
        pixels away from the edge.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        # --- Manage Scrolling ---
        new_position = arcade.camera.grips.constrain_boundary_xy(
            self.camera_sprites.view_data, CAMERA_BOUNDARY, self.player_sprite.position
        )

        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position,
            (new_position[0], new_position[1]),
            CAMERA_SPEED,
        )

    def on_resize(self, width: int, height: int):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        super().on_resize(width, height)
        self.camera_sprites.match_window()
        self.camera_gui.match_window(position=True)


def main():
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
