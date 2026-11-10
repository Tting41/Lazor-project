"""DFS search and verification. Assigned module owner: Junying Yu."""
from blocks import BLOCK_TYPES, MOVABLE, EMPTY
from simulation import trace, reachable

class Solver:
    """
    Depth-first search over the cells the lasers actually touch.

    **Parameters**

        board: *Board*
    """

    def __init__(self, board):
        self.board = board
        self.nodes = 0

    def solve(self):
        """
        Find a solution.

        **Returns**

            cells: *list of Block* or None
                Fully decided cell list, or None if the board has no
                solution.
        """
        cells = list(self.board.cells)
        remaining = dict((k, self.board.blocks.get(k, 0))
                         for k in BLOCK_TYPES)
        self.nodes = 0
        if self._search(cells, remaining, cells.count(None)):
            return cells
        return None

    def _search(self, cells, remaining, n_unknown):
        self.nodes += 1
        left = remaining['A'] + remaining['B'] + remaining['C']
        if left > n_unknown:           # not enough room for every block
            return False

        points, idx = trace(self.board, cells)

        if idx is None:
            if not self.board.targets <= points:
                return False
            # Lasers are settled; drop leftover blocks on untouched cells
            # (they cannot affect the lasers) and mark the rest empty.
            spare = [i for i, c in enumerate(cells) if c is None]
            k = 0
            for kind in BLOCK_TYPES:
                for _ in range(remaining[kind]):
                    cells[spare[k]] = MOVABLE[kind]
                    k += 1
            for i in spare[k:]:
                cells[i] = EMPTY
            return True

        # Prune: give up if some target can no longer be reached.
        targets = self.board.targets
        if not targets <= points:
            can_turn = remaining['A'] + remaining['C'] > 0
            if not targets <= reachable(self.board, cells, can_turn):
                return False

        # Branch on the first undecided cell a laser touches.
        cells[idx] = EMPTY
        if self._search(cells, remaining, n_unknown - 1):
            return True
        for kind in BLOCK_TYPES:
            if remaining[kind]:
                cells[idx] = MOVABLE[kind]
                remaining[kind] -= 1
                if self._search(cells, remaining, n_unknown - 1):
                    return True
                remaining[kind] += 1
        cells[idx] = None
        return False

def verify(board, cells):
    """Return True if ``cells`` is a complete, valid solution."""
    if any(c is None for c in cells):
        return False
    used = {}
    for c, orig in zip(cells, board.cells):
        if orig is None and c.symbol in BLOCK_TYPES:
            used[c.symbol] = used.get(c.symbol, 0) + 1
    want = dict((k, v) for k, v in board.blocks.items() if v)
    if used != want:
        return False
    points, _ = trace(board, cells)
    return board.targets <= points
