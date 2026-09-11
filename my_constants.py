import arcade

import function_file
import gameview_file

# ==================================
# --- PHYSICS ----
# ==================================
# (float) constant downward acceleration
# NOTE: represented by the letter g in physics
GRAVITATIONAL_ACCELERATION = 0.4

# (float) decrease DRAG_COEFFICIENT = player hovers over the apex of their jump arc for longer. Player is slower at the top of their bounce.
# NOTE: In real life, the drag coefficient usually has a positive value; acceleration's magntiude DECREASES if speed INCREASES. In this game, I made it a negative value so that acceleration's magnitude INCREASES if speed INCREASES
# NOTE: represented by the letter b in physics
DRAG_COEFFICIENT = -0.03

# (float) how much energy the player conserves during a bounce.
# 1 = no energy is lost. The player will bounce back to their original y-position.
# 0 = all energy is lost on a bounce. The player hits the pad and loses all of their velocity_y.
BOUNCE_DECAY_CONSTANT = 0.45

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
    sound (Sound): playable sound
        .wav works
        .ogg doesn't work
"""
pad = {
    "name": "pad",
    # pad's image_scale causes bugs. if the pad is too small compared to the target, spike, and coin, then the program breaks.
    "image_scale": 1.15,
    # (int) x-displacement between adjacent pads
    "delta_x": 800,
    # (int) y-displacement between adjacent pads
    "delta_y": 200,
    # (floats) the first 4 starting pads will spawn with x values in between these two bounds
    # NOTE: Currently, the bounds enclose the middle one third of the screen
    "start_x_min": int(gameview_file.GameView.internal_width / 4),
    "start_x_max": int(gameview_file.GameView.internal_width * 3 / 4),
    # (int) Kill the player after they go MIN_PLAYER_PAD_HEIGHT_DIFFERENCE pixels underneath a pad.
    "MIN_PLAYER_PAD_HEIGHT_DIFFERENCE": 0,
    "sound": arcade.load_sound(":resources:/sounds/coin1.wav"),
}

target = {
    "name": "target",
    "image_scale": 1,
    "spawn_rate": 0.25,
    "height from pad": 25,
    "sound": arcade.load_sound(":resources:/sounds/coin2.wav"),
}

coin = {
    "name": "coin",
    "image_scale": 0.66,
    "spawn_rate": 1,  # 0.15,
    "height from pad": 150,
    # if the user gets over the max number of coins, then they will earn a party!
    "party_count": 12,
    "sound": arcade.load_sound(":resources:/sounds/coin3.wav"),
    "seconds_per_party": 6.5,
}

spike = {
    "name": "spike",
    "image_scale": 2,
    "spawn_rate": function_file.asymptotic_function(
        x=function_file.bounce_count, max_y=1.5, x_at_half_y=50
    )
    * 0.07,  # goes from 0.7 to 0.7 * max_y
    "height from pad": 30,
}

player = {
    "name": "player",
    "image_scale": 2,
}

# ==================================
# --- IDK ---
# ==================================
game_speed_factor_party = 4.5
game_speed_function = function_file.asymptotic_function(
    x=function_file.bounce_count, max_y=4.5, x_at_half_y=80
)
# ==================================
# --- OTHER ---
# ==================================


death_sound = arcade.load_sound(":resources:/sounds/coin4.wav")

instruction_text = "Left click = start, Esc = close, F = fullscreen"
