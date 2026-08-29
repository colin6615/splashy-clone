GRAVITATIONAL_ACCELERATION = .2
    # good value = .05
    # constant downward acceleration
    # represented by the letter g in physics
DRAG_COEFFICIENT = 0
    # good value = -0.2
    # decrease DRAG_COEFFICIENT = player hovers over the apex of their jump arc for longer. Player is slower at the top of their bounce. 
    # represented by the letter b in physics
    # In real life, the drag coefficient usually has a positive value; acceleration's magntiude DECREASES if speed INCREASES. In this game, I made it a negative value so that acceleration's magnitude INCREASES if speed INCREASES

BOUNCE_DECAY_CONSTANT = 0.1
    # good value = 0.7
     # how much energy the player conserves during a bounce.
     # 1 = no energy is lost. The player will bounce back to their original y-position.
     # 0 = all energy is lost on a bounce. The player hits the box and loses all of their velocity.
X_ALL_BOXES = 4 
    # the x-position of all boxes
DELTA_Y = 3
    # y-distance between boxes