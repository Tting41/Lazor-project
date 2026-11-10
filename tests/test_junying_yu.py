"""Tests for the modules assigned to Junying Yu."""
import os
import random
import tempfile
import time
import unittest
import lazor
from lazor import (Board, BFFError, Solver, trace, verify, EMPTY, NO_BLOCK,
                   MOVABLE, ReflectBlock, OpaqueBlock, RefractBlock)
from tests.support import MAD_1, brute_force, random_board

class TestSolver(unittest.TestCase):

    def test_mad_1(self):
        b = Board.from_file(MAD_1)
        cells = Solver(b).solve()
        self.assertIsNotNone(cells)
        self.assertTrue(verify(b, cells))

    def test_unsolvable(self):
        b = Board.from_string('GRID START\no\nGRID STOP\nB 1\n'
                              'L 0 1 1 1\nP 2 1\n')
        self.assertIsNone(Solver(b).solve())

    def test_fixed_blocks_untouched(self):
        b = Board.from_string('GRID START\no A o\no o o\nGRID STOP\n'
                              'A 1\nL 0 1 1 1\nP 1 2\n')
        cells = Solver(b).solve()
        self.assertIs(cells[1], lazor.FIXED['A'])

    def test_matches_brute_force(self):
        """DFS and brute force must agree on random small boards."""
        rng = random.Random(1)
        for _ in range(150):
            b = random_board(rng, rng.randint(2, 3), rng.randint(2, 3),
                             rng.randint(1, 3), rng.randint(1, 4))
            # Some random targets make a different placement necessary,
            # so also shuffle targets to create unsolvable cases.
            if rng.random() < 0.3:
                b.targets.add((rng.randrange(2 * b.width + 1),
                               rng.randrange(2 * b.height + 1)))
            fast = Solver(b).solve()
            slow = brute_force(b)
            self.assertEqual(fast is None, slow is None)
            if fast is not None:
                self.assertTrue(verify(b, fast))

    def test_speed_on_large_boards(self):
        rng = random.Random(7)
        for _ in range(10):
            b = random_board(rng, 6, 6, 8, 6)
            start = time.perf_counter()
            cells = Solver(b).solve()
            self.assertLess(time.perf_counter() - start, 5)
            self.assertTrue(verify(b, cells))

class TestOutput(unittest.TestCase):

    def test_writes_files(self):
        with tempfile.TemporaryDirectory() as d:
            board, cells, _ = lazor.solve_file(MAD_1, d)
            txt = os.path.join(d, 'mad_1_solution.txt')
            with open(txt) as f:
                text = f.read()
            # The solution file is itself a valid grid section.
            parsed = Board.from_string(text + 'L 2 7 1 -1\nP 3 0\n')
            self.assertEqual(parsed.width, 4)
            self.assertTrue(os.path.exists(
                os.path.join(d, 'mad_1_solution.png')))
