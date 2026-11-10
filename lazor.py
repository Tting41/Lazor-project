"""Compatibility entry point: preserve the original CLI and import names.

Assigned integration owner: Junying Yu.
All implementation now lives in the separate team modules.
"""
import sys
from blocks import (Block, EmptyCell, NoBlockCell, ReflectBlock, OpaqueBlock,
                    RefractBlock, EMPTY, NO_BLOCK, MOVABLE, FIXED, BLOCK_TYPES)
from board import Board, BFFError
from simulation import trace, reachable
from solver import Solver, verify
from output import solution_text, write_text, write_png
from main import solve_file, main

if __name__ == '__main__':
    sys.exit(main())
