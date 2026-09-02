import arcade


class Item(arcade.Sprite):
    def _update(self, delta_time):  # **kwargs
        # children will overide this to inserrt their specific code
        pass

    def update(self, delta_time):  # **kwargs
        # Run general item stuff

        # Call the child's specific logic
        self._update(delta_time)  # **kwargs
