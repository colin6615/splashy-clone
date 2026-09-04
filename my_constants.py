import arcade

# other
WINDOW_WIDTH = 1147
WINDOW_HEIGHT = 625

# ==================================
# --- PHYSICS ----
# ==================================
# (float) constant downward acceleration
# NOTE: represented by the letter g in physics
GRAVITATIONAL_ACCELERATION = 0.07  # good value = .07

# (float) decrease DRAG_COEFFICIENT = player hovers over the apex of their jump arc for longer. Player is slower at the top of their bounce.
# NOTE: In real life, the drag coefficient usually has a positive value; acceleration's magntiude DECREASES if speed INCREASES. In this game, I made it a negative value so that acceleration's magnitude INCREASES if speed INCREASES
# NOTE: represented by the letter b in physics
DRAG_COEFFICIENT = -0.01  # good value = -0.01

# (float) how much energy the player conserves during a bounce.
# 1 = no energy is lost. The player will bounce back to their original y-position.
# 0 = all energy is lost on a bounce. The player hits the pad and loses all of their velocity.
BOUNCE_DECAY_CONSTANT = 0.6  # good value = 0.6

# (float) speeds up the game after every bounce.
# NOTE: 0 = no speed change
# NOTE: starting self.time_factor is 1, so after the n-th bounce, it updates to self.time_factor + TIME_FACTOR_CHANGE * N
TIME_FACTOR_CHANGE = 0.01

# ==================================
# --- item dictionaries ---
# ==================================
"""
Explanations of common dictionary keys:
    image_path (str): path to sprite image
    image_scale (float): scales size of image. 
    spawn_rate (float): probablility that the item will spawn on a pad
        spawn_rate = 1 means that the item will spawn on every pad.
    height from pad (int): difference in y positions of pad and item
"""
pad = {
    "image_path": "assets/green_rectangle.png",
    "image_scale": 0.5,
    # (int) x-displacement between adjacent pads
    # NOTE: good value is 100
    "delta_x": 200,
    # (int) y-displacement between adjacent pads
    # NOTE: good value is 100
    "delta_y": 128,
    # (floats) the first 4 starting pads will spawn with x values in between these two bounds
    # NOTE: Currently, the bounds enclose the middle one third of the screen
    "start_min": int(WINDOW_WIDTH / 3),
    "start_max": int(WINDOW_WIDTH * 2 / 3),
    # (int) Kill the player after they go MIN_PLAYER_PAD_HEIGHT_DIFFERENCE pixels underneath a pad.
    "MIN_PLAYER_PAD_HEIGHT_DIFFERENCE": 0,
}

target = {
    "image_path": "assets/target.png",
    "image_scale": 1,
    "spawn_rate": 0.3,
    "height from pad": 0,
}

coin = {
    "image_path": "assets/gold_1.png",
    "image_scale": 0.33,
    "spawn_rate": 0.2,
    "height from pad": 50,
}

spike = {
    "image_path": "assets/spike.png",
    "image_scale": 1,
    "spawn_rate": 1,
    "height from pad": 12,
}

# list of item dictionaries
# NOTE: excludes pad
items_close_to_pad_dicts = [target, coin, spike]
item_dicts = [target, pad, coin, spike]
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
# camera
# If the player moves further than this boundary away from the camera we use a
# constraint to move the camera
HORIZONTAL_BOUNDARY = WINDOW_WIDTH / 2.0  # float
BOTTOM_BOUNDARY = 0  # float
TOP_BOUNDARY = WINDOW_HEIGHT / 2.0 - 100  # float

# (float) How fast the camera pans to the player.
# NOTE: 1.0 is instant.
CAMERA_SPEED = 0.6
