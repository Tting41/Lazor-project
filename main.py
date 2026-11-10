"""Command-line integration. Assigned module owner: Junying Yu."""
import argparse
import os
import sys
import time
from board import Board, BFFError
from solver import Solver
from output import solution_text, write_text, write_png

def solve_file(path, outdir=None, png=True):
    """
    Solve one .bff file and write the outputs.

    **Returns**

        (board, cells, elapsed)  -- ``cells`` is None if unsolvable.
    """
    board = Board.from_file(path)
    start = time.perf_counter()
    cells = Solver(board).solve()
    elapsed = time.perf_counter() - start
    if cells is not None:
        outdir = outdir or os.path.dirname(os.path.abspath(path))
        os.makedirs(outdir, exist_ok=True)
        base = os.path.join(outdir, board.name + '_solution')
        write_text(board, cells, base + '.txt', elapsed)
        if png:
            write_png(board, cells, base + '.png')
    return board, cells, elapsed

def main(argv=None):
    """Entry point for ``python lazor.py``."""
    parser = argparse.ArgumentParser(description='Solve Lazor boards.')
    parser.add_argument('files', nargs='+', help='.bff board files')
    parser.add_argument('--outdir', help='where to write solutions '
                        '(default: next to each .bff file)')
    parser.add_argument('--no-png', action='store_true',
                        help='skip writing PNG images')
    args = parser.parse_args(argv)

    status = 0
    for path in args.files:
        try:
            board, cells, elapsed = solve_file(path, args.outdir,
                                               not args.no_png)
        except (OSError, BFFError) as e:
            print('%s: error: %s' % (path, e), file=sys.stderr)
            status = 1
            continue
        if cells is None:
            print('%s: no solution found (%.3f s)' % (path, elapsed))
            status = 1
        else:
            print('%s: solved in %.4f s' % (path, elapsed))
            print(solution_text(board, cells))
            print()
    return status


if __name__ == "__main__":
    sys.exit(main())
