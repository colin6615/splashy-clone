import arcade

# ==================================
# --- PHYSICS ----
# ==================================
# constant downward acceleration
# represented by the letter g in physics
GRAVITATIONAL_ACCELERATION = 1  # good value = .07

# In real life, the drag coefficient usually has a positive value; acceleration's magntiude DECREASES if speed INCREASES. In this game, I made it a negative value so that acceleration's magnitude INCREASES if speed INCREASES
# decrease DRAG_COEFFICIENT = player hovers over the apex of their jump arc for longer. Player is slower at the top of their bounce.
# represented by the letter b in physics
DRAG_COEFFICIENT = -0.01  # good value = -0.01

# how much energy the player conserves during a bounce.
# 1 = no energy is lost. The player will bounce back to their original y-position.
# 0 = all energy is lost on a bounce. The player hits the pad and loses all of their velocity.
BOUNCE_DECAY_CONSTANT = 0.6  # good value = 0.6

# speeds up the game after every bounce.
# 0 = no speed change
# starting self.time_factor is 1, so after the n-th bounce, it updates to self.time_factor + TIME_FACTOR_CHANGE * N
TIME_FACTOR_CHANGE = 0.01

# ==================================
# --- item dictionaries ---
# ==================================

pad = {
    "image_path": "assets/green_rectangle.png",  # path to sprite image
    "image_scale": 0.5,  # scales size of image. should be 0.5
    # x-displacement between adjacent pads
    # NOTE: good value is 100
    "delta_x": 200,
    # y-displacement between adjacent pads
    # NOTE: good value is 100
    "delta_y": 128,
}


target = {
    "image_path": "assets/target.png",
    "image_scale": 1,
}

# list of item dictionaries
item_dicts = [pad, target]

# add sprite width entry to each dictionary
for dictionary in item_dicts:
    # load texture from image
    texture = arcade.load_texture(dictionary["image_path"])

    # get width_height tuple
    width_height = texture.size

    # sprite width = image width * image scale
    dictionary["width"] = width_height[0] * dictionary["image_scale"]

# ==================================
# --- COIN ---
# ==================================
SPRITE_SCALING = 0.5
SPRITE_SCALING_COIN = 0.3
NUMBER_OF_COINS = 50

# ==================================
# --- OTHER ---
# ==================================
# other
WINDOW_WIDTH = 1147
WINDOW_HEIGHT = 625

# camera
# If the player moves further than this boundary away from the camera we use a
# constraint to move the camera
HORIZONTAL_BOUNDARY = WINDOW_WIDTH / 2.0
BOTTOM_BOUNDARY = 0
TOP_BOUNDARY = WINDOW_HEIGHT / 2.0 - 100

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.6
