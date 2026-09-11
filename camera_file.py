"""placeholder."""

import arcade

import gameview_file
import player_file

# (float) How fast the camera pans to the player.
# NOTE: 1.0 is instant.
CAMERA_SPEED = 0.6


class My_camera:
    def setup(self):
        """make the cameras. Create camera width as class variable."""

        # make the camerea for the sprites.
        self.camera_sprites = arcade.Camera2D(
            position=(0, 0),
            projection=arcade.types.LRBT(
                left=0,
                right=gameview_file.GameView.internal_width,
                bottom=0,
                top=gameview_file.GameView.INERNAL_HEIGHT,
            ),
            viewport=self.window.rect,
        )
        # make camera for the gui
        self.camera_gui = arcade.Camera2D(
            position=(0, 0),
            projection=arcade.types.LRBT(
                left=0,
                right=gameview_file.GameView.internal_width,
                bottom=0,
                top=gameview_file.GameView.INERNAL_HEIGHT,
            ),
            viewport=self.window.rect,
        )

        # make a boundary for camera scrolling. It's difficult for the player, but not the background objects, to move past this boundary. If the player moves past this boundary, then the camera moves with the player.
        # top boundary must be greater than the bottom boundary, or else it looks weird
        # top boundary > bottom boundary
        self.camera_boundary = arcade.LRBT(
            -2000,
            2000,
            gameview_file.GameView.INERNAL_HEIGHT * 0.68,  # bottom boundary
            gameview_file.GameView.INERNAL_HEIGHT * 0.86,  # Top boundary
        )
        My_camera.viewport_width = self.width

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
            self.camera_boundary,
            player_file.Player.sprite.position,
        )

        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position,
            (new_position[0], new_position[1]),
            CAMERA_SPEED,
        )

    def _on_key_press(self, key, modifiers):
        """toggle fullscreen when you press F."""

        if key == arcade.key.F:
            # Flip between full and not full screen.
            self.window.set_fullscreen(not self.window.fullscreen)

            # update window width to match the user's aspect ratio. Ex: some people might have 16:9 sized screens.
            USERS_ASPECT_RATIO = self.width / self.height
            gameview_file.GameView.internal_width = (
                gameview_file.GameView.INERNAL_HEIGHT * USERS_ASPECT_RATIO
            )

            # Write procjections. This controls sprite and gui size relative to the window
            self.camera_sprites.projection = arcade.types.LRBT(
                left=0,
                right=gameview_file.GameView.internal_width,
                bottom=0,
                top=gameview_file.GameView.INERNAL_HEIGHT,
            )
            self.camera_gui.projection = arcade.types.LRBT(
                left=0,
                right=gameview_file.GameView.internal_width,
                bottom=0,
                top=gameview_file.GameView.INERNAL_HEIGHT,
            )

            # write viewports. This controls the projections' size relative to the screen.
            self.camera_sprites.viewport = self.window.rect

            self.camera_gui.viewport = self.window.rect

            My_camera.viewport_width = self.width
