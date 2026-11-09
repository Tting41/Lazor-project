"""Laser tracing and reachability. Assigned module owner: Tingting Li."""
from blocks import MOVABLE, EMPTY
from laser import next_cell_center

def trace(board, cells, record_path=False):
    """
    Follow every laser through ``cells``.

    **Parameters**

        board: *Board*
        cells: *list*
            Row-major cell list; ``None`` means "undecided".
        record_path: *bool*
            If True, also return the list of beam segments for drawing.

    **Returns**

        points: *set of (x, y)*
            Lattice points the lasers passed through.
        unknown: *int or None*
            Index of the first undecided cell a laser touched, or None if
            the lasers never touched an undecided cell.  Tracing stops as
            soon as one is found.
        segments: *list*  (only if ``record_path``)
            ``[(x0, y0, x1, y1), ...]``
    """
    w = board.width
    max_x = 2 * w
    max_y = 2 * board.height
    seen = set()
    points = set()
    segments = []
    stack = list(board.lasers)

    while stack:
        x, y, vx, vy = stack.pop()
        while 0 <= x <= max_x and 0 <= y <= max_y:
            state = (x, y, vx, vy)
            if state in seen:          # beam loops or merges: done
                break
            seen.add(state)
            points.add((x, y))

            cx, cy = next_cell_center(x, y, vx, vy)
            if 0 <= cx < max_x and 0 <= cy < max_y:
                idx = (cy >> 1) * w + (cx >> 1)
                cell = cells[idx]
                if cell is None:
                    if record_path:
                        return points, idx, segments
                    return points, idx
                dirs = cell.interact(x, vx, vy)
            else:
                dirs = ((vx, vy),)     # looking off the edge of the board

            if not dirs:
                break
            for dx, dy in dirs[1:]:    # extra beam from a refract block
                stack.append((x + dx, y + dy, dx, dy))
                if record_path:
                    segments.append((x, y, x + dx, y + dy))
            vx, vy = dirs[0]
            if record_path:
                segments.append((x, y, x + vx, y + vy))
            x += vx
            y += vy

    if record_path:
        return points, None, segments
    return points, None

def reachable(board, cells, can_turn):
    """
    Over-estimate every point a laser could still reach.

    Undecided cells are treated as "could be anything": the laser may
    pass straight through and, if ``can_turn``, may also be reflected.
    Decided cells behave normally.  If a target is not in the returned
    set, no way of filling the undecided cells can ever hit it, so the
    solver can abandon the branch.

    **Parameters**

        board: *Board*
        cells: *list*
        can_turn: *bool*
            True if a reflect or refract block is still available.

    **Returns**

        points: *set of (x, y)*
    """
    w = board.width
    max_x = 2 * w
    max_y = 2 * board.height
    turner = MOVABLE['C']
    seen = set()
    points = set()
    stack = list(board.lasers)

    while stack:
        x, y, vx, vy = stack.pop()
        while 0 <= x <= max_x and 0 <= y <= max_y:
            state = (x, y, vx, vy)
            if state in seen:
                break
            seen.add(state)
            points.add((x, y))

            cx, cy = next_cell_center(x, y, vx, vy)
            if 0 <= cx < max_x and 0 <= cy < max_y:
                cell = cells[(cy >> 1) * w + (cx >> 1)]
                if cell is None:
                    # pass + reflect is exactly what a refract block does
                    cell = turner if can_turn else EMPTY
                dirs = cell.interact(x, vx, vy)
            else:
                dirs = ((vx, vy),)

            if not dirs:
                break
            for dx, dy in dirs[1:]:
                stack.append((x + dx, y + dy, dx, dy))
            vx, vy = dirs[0]
            x += vx
            y += vy
    return points
