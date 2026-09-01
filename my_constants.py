# ==================================
# --- PHYSICS ----
# ==================================
# constant downward acceleration
# represented by the letter g in physics
GRAVITATIONAL_ACCELERATION = 0.07  # good value = .05

# In real life, the drag coefficient usually has a positive value; acceleration's magntiude DECREASES if speed INCREASES. In this game, I made it a negative value so that acceleration's magnitude INCREASES if speed INCREASES
# decrease DRAG_COEFFICIENT = player hovers over the apex of their jump arc for longer. Player is slower at the top of their bounce.
# represented by the letter b in physics
DRAG_COEFFICIENT = -0.01  # good value = -0.2

# how much energy the player conserves during a bounce.
# 1 = no energy is lost. The player will bounce back to their original y-position.
# 0 = all energy is lost on a bounce. The player hits the pad and loses all of their velocity.
BOUNCE_DECAY_CONSTANT = 0.7  # good value = 0.7

# speeds up the game after every bounce.
# 0 = no speed change
# starting self.time_factor is 1, so after the n-th bounce, it updates to self.time_factor + TIME_FACTOR_CHANGE * N
TIME_FACTOR_CHANGE = 0.01

# ==================================
# --- PADS ---
# ==================================
# the x-position of starting pads
X_ALL_PADS = 10

# x-displacement between non-starting pads
MOVE_PAD_X = 100

# y-distance between pads.
DELTA_Y = 2  # int

SPRITE_SCALING_PAD = 0.5
PAD_LENGTH = 64

# ==================================
# --- COIN ---
# ==================================
SPRITE_SCALING = 0.5
SPRITE_SCALING_COIN = 0.3
NUMBER_OF_COINS = 50

# ==================================
# --- OTHER ---
# ==================================
WINDOW_WIDTH = 1147
WINDOW_HEIGHT = 625
