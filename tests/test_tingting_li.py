"""Tests for the modules assigned to Tingting Li."""
import os
import random
import tempfile
import time
import unittest
import lazor
from lazor import (Board, BFFError, Solver, trace, verify, EMPTY, NO_BLOCK,
                   MOVABLE, ReflectBlock, OpaqueBlock, RefractBlock)
from tests.support import MAD_1, brute_force, random_board

class TestTrace(unittest.TestCase):

    def board(self, grid, laser, w, h):
        return Board(w, h, grid, {}, [laser], {(0, 0)})

    def test_empty_board_straight_line(self):
        b = self.board([EMPTY] * 4, (0, 1, 1, 1), 2, 2)
        points, unknown = trace(b, b.cells)
        self.assertIsNone(unknown)
        self.assertEqual(points, {(0, 1), (1, 2), (2, 3), (3, 4)})

    def test_reflect_bounces_back(self):
        # Laser going right into a reflect block's left face.
        b = self.board([EMPTY, MOVABLE['A']], (2, 1, 1, 1), 2, 1)
        points, _ = trace(b, b.cells)
        self.assertIn((1, 2), points)
        self.assertNotIn((3, 2), points)

    def test_opaque_stops(self):
        b = self.board([EMPTY, MOVABLE['B']], (2, 1, 1, 1), 2, 1)
        points, _ = trace(b, b.cells)
        self.assertEqual(points, {(2, 1)})

    def test_refract_splits(self):
        b = self.board([EMPTY, MOVABLE['C']], (2, 1, 1, 1), 2, 1)
        points, _ = trace(b, b.cells)
        self.assertIn((3, 2), points)   # passed through
        self.assertIn((1, 2), points)   # reflected

    def test_stops_at_unknown(self):
        b = self.board([None, None], (0, 1, 1, 1), 2, 1)
        self.assertEqual(trace(b, b.cells)[1], 0)

    def test_loop_terminates(self):
        # Reflect blocks all around a closed loop must not hang.
        a = MOVABLE['A']
        cells = [a, a, a, a, EMPTY, a, a, a, a]
        b = self.board(cells, (2, 3, 1, 1), 3, 3)
        trace(b, cells)
