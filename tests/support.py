"""Shared random-board and reference-search helpers."""
import itertools
import os
from lazor import Board, trace, EMPTY, NO_BLOCK, MOVABLE

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAD_1 = os.path.join(HERE, "boards", "mad_1.bff")

def brute_force(board):
    """Try every placement.  Slow; only for checking small boards."""
    free = [i for i, c in enumerate(board.cells) if c is None]
    kinds = []
    for k in 'ABC':
        kinds += [k] * board.blocks.get(k, 0)
    for chosen in itertools.permutations(free, len(kinds)):
        cells = [EMPTY if c is None else c for c in board.cells]
        for i, k in zip(chosen, kinds):
            cells[i] = MOVABLE[k]
        if board.targets <= trace(board, cells)[0]:
            return cells
    return None

def random_board(rng, w, h, n_blocks, n_targets, x_frac=0.15):
    """
    Build a random board that is solvable by construction: place random
    blocks, trace the laser, and pick targets from the points it hits.
    """
    while True:
        cells = [NO_BLOCK if rng.random() < x_frac else None
                 for _ in range(w * h)]
        free = [i for i, c in enumerate(cells) if c is None]
        if len(free) < n_blocks:
            continue
        kinds = [rng.choice('AAABC') for _ in range(n_blocks)]
        solved = [EMPTY if c is None else c for c in cells]
        for i, k in zip(rng.sample(free, n_blocks), kinds):
            solved[i] = MOVABLE[k]
        # laser starts on the left edge at an odd y
        y = 2 * rng.randrange(h) + 1
        lasers = [(0, y, 1, rng.choice((-1, 1)))]
        blocks = {}
        for k in kinds:
            blocks[k] = blocks.get(k, 0) + 1
        board = Board(w, h, cells, blocks, lasers, set())
        points = sorted(trace(board, solved)[0])
        if len(points) < n_targets:
            continue
        board.targets = set(rng.sample(points, n_targets))
        return board
