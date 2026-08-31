import arcade


class Player(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        """ Constructor. """
        # Call the parent class (Sprite) constructor
        super().__init__(filename, sprite_scaling)
        
    def setup():
        Player.list = None
        Player.sprite = None
        Player.list = arcade.SpriteList()
        Player.sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            scale=0.4,
        )
        Player.sprite.center_x = 256
        Player.sprite.center_y = 0
        Player.sprite.velocity = 0
        Player.list.append(Player.sprite)


"""

class Player:
    def __init__(self, filename, sprite_scaling):

        # Call the parent class (Sprite) constructor
        super().__init__(filename, sprite_scaling)
        # set position
        self.center_x = 256
        self.center_y = 0

    def setup():
        Player.list = None
        Player.list = arcade.SpriteList()
        Player.player = 
        Player.list.append(Player.player)

"""
