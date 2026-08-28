import random
import arcade
import math

SPRITE_SCALING = 3
# --- Constants ---
COIN_COUNT = 30
SPRITE_SCALING_PLAYER = 2.5
SPRITE_SCALING_COIN = 1.5

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600


class Coin(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        """ Constructor. """
        # Call the parent class (Sprite) constructor
        super().__init__(filename, sprite_scaling)

        # Current angle in radians
        self.circle_angle = 0

        # How far away from the center to orbit, in pixels
        self.circle_radius = 0

        # How fast to orbit, in radians per frame
        self.circle_speed = 0.01

        # Set the center of the point we will orbit around
        self.circle_center_x = 0
        self.circle_center_y = 0

    def update(self, delta_time):

        """ Update the ball's position. """
        # Calculate a new x, y
        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
            + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) \
            + self.circle_center_y

        # Increase the angle in prep for the next round.
        self.circle_angle += self.circle_speed

class Bad_coin(arcade.Sprite):
    """
    These coins will reduce your score!
    """

    def reset_pos(self):

        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self, delta_time):

        # Move the coin
        self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_pos()

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):

        super().__init__(width, height)

        # Sprite lists
        self.player_list = None
        self.coin_list = None
        self.bad_coin_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None

        # load sounds from the Kenney website (https://kenney.nl/assets/sci-fi-sounds)
        self.coin_01_sound = arcade.load_sound("assets/coin_01.ogg")
        self.bad_coin_sound = arcade.load_sound("assets/coin_01.ogg")


    def start_new_game(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bad_coin_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        # Character image from Kenney website: https://kenney.nl
        self.player_sprite = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from Kenney website: https://kenney.nl
            coin = Coin(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

            # Position the center of the circle the coin will orbit
            coin.circle_center_x = random.randrange(SCREEN_WIDTH)
            coin.circle_center_y = random.randrange(SCREEN_HEIGHT)

            # Random radius from 10 to 200
            coin.circle_radius = random.randrange(10, 200)

            # Random start angle from 0 to 2pi
            coin.circle_angle = random.random() * 2 * math.pi

            # Add the coin to the lists
            self.coin_list.append(coin)

        for i in range(COIN_COUNT):


            # Create the coin instance
            # Coin image from Kenney website: https://kenney.nl
            bad_coin = Bad_coin(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

            # Position the coin
            bad_coin.center_x = random.randrange(SCREEN_WIDTH)
            bad_coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the bad_coin to the lists
            self.bad_coin_list.append(bad_coin)

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.coin_list.draw()
        self.bad_coin_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = "Score: " + str(self.score)
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        if len(self.coin_list) <= 0:
            arcade.draw_text("Game Over",
                                        300, 300,
                                        arcade.color.BLACK, 80)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        if len(self.coin_list) > 0:
            self.coin_list.update(delta_time)
            self.bad_coin_list.update(delta_time)
 

        # Generate a list of all sprites that collided with the player.
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_list)
        bad_coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.bad_coin_list)

        # Loop through each colliding sprite, remove it, and add to the score. play sound
        for coin in coin_hit_list:
            self.score += 1
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.coin_01_sound)

        # same thing, but remove score if it's a bad coin.
        for bad_coin in bad_coin_hit_list:
            self.score -= 1
            bad_coin.remove_from_sprite_lists()
            arcade.play_sound(self.bad_coin_sound)


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.start_new_game()
    arcade.run()


if __name__ == "__main__":
    main()