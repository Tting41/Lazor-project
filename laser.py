"""Collision geometry. Assigned module owner: Tingting Li."""


def next_cell_center(x, y, vx, vy):
    """Return the half-step coordinates of the cell being entered.

    At a horizontal edge x is odd; at a vertical edge x is even.
    The returned centre can lie outside the board for an outgoing ray.
    """
    if x & 1:
        return x, y + vy
    return x + vx, y
