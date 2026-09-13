# Source - https://stackoverflow.com/a/10987177
# Posted by Hugh Bothwell
# Retrieved 2026-09-13, License - CC BY-SA 3.0


pad_image_1 = "image_path_1"
pad_image_2 = "image_path_2"

import itertools

pad_image_iterator = itertools.cycle([pad_image_1, pad_image_2])
current_pad_image = next(pad_image_iterator)
print(current_pad_image)
