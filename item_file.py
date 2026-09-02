import arcade


class Item(arcade.Sprite):
    def _update(self):  # **kwargs
        # children will overide this to inserrt their specific code
        pass

    def update(self):  # **kwargs
        # Run general item stuff

        # Call the child's specific logic
        self._update()  # **kwargs
