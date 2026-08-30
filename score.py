# Source - https://stackoverflow.com/a/16726646
# Posted by elyase, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-29, License - CC BY-SA 4.0
import shelve

import numpy as np

score_shelf = shelve.open("score.txt")  # here you will save the score variable
# check if array exists
try:
    score_array = np.append(score_array, 2)
# if no array exists, then make empty array
except NameError:
    score_array = np.array((0, 0))
else:
    pass

score_shelf["score"] = score_array  # write score array to disk

# player loses
end_screen_title = score_shelf["score"]  # read score from disk
# print score
print(
    f"array: {end_screen_title}\n previous: {end_screen_title[-1]}\n top: {max(end_screen_title)}"
)

"""
def add_to_score():
    try:
        score_shelf = shelve.open("score.txt")  # here you will save the score variable
        score_array.append(3)
    except: 
        score_array = np.array(())
    else:
        pass
    score_shelf["score"] = score_array  # write sample scores to disk

    # player loses
    end_screen_title = d["score"]  # the score is read from disk
    print(
        f"array: {end_screen_title}\n previous: {end_screen_title[-1]}\n top: {max(end_screen_title)}"
    )

score_shelf.close()
"""
