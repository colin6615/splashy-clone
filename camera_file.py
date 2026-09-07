import arcade

import my_constants
import player_file

CAMERA_BOUNDARY = arcade.LRBT(
    -my_constants.HORIZONTAL_BOUNDARY,
    my_constants.HORIZONTAL_BOUNDARY,
    -my_constants.BOTTOM_BOUNDARY,
    my_constants.TOP_BOUNDARY,
)


class my_camera:
    def setup(self):
        # camera stuff
        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()


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
            self.camera_sprites.view_data,
            CAMERA_BOUNDARY,
            player_file.Player.sprite.position,
        )

        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position,
            (new_position[0], new_position[1]),
            my_constants.CAMERA_SPEED,
        )
