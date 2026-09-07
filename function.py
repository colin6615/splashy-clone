def asymptotic_function(x, max_y, x_at_half_y):
    """
    inputs 3 numbers and outputs 1 number.

    Args:
        x (float): input variable
        max_y (float): maximum output
            reached at infinity
            asymptotic_function(x = infinity) = max_y
        x_at_half_y (float): At this x value, output is  (sort of) halfway maxed out.
            asymptotic_function(x = x_at_half_y) = [(max_y - 1) / 2] + 1
    Returns:
        output (float)
    """

    numerator = (max_y - 1) * x
    denominator = x + x_at_half_y
    y = 1 + numerator / denominator
    return y