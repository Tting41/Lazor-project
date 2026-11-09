"""Tests for the modules assigned to Jiakai Chen."""
import os
import random
import tempfile
import time
import unittest
import lazor
from lazor import (Board, BFFError, Solver, trace, verify, EMPTY, NO_BLOCK,
                   MOVABLE, ReflectBlock, OpaqueBlock, RefractBlock)
from tests.support import MAD_1, brute_force, random_board

class TestBlocks(unittest.TestCase):

    def test_reflect(self):
        b = ReflectBlock()
        self.assertEqual(b.interact(3, 1, 1), ((1, -1),))   # top face
        self.assertEqual(b.interact(2, 1, 1), ((-1, 1),))   # side face

    def test_opaque(self):
        self.assertEqual(OpaqueBlock().interact(3, 1, 1), ())

    def test_refract(self):
        self.assertEqual(RefractBlock().interact(3, 1, -1),
                         ((1, -1), (1, 1)))

    def test_fixed_flag(self):
        self.assertTrue(lazor.FIXED['A'].fixed)
        self.assertFalse(lazor.MOVABLE['A'].fixed)

class TestParsing(unittest.TestCase):

    def test_mad_1(self):
        b = Board.from_file(MAD_1)
        self.assertEqual((b.width, b.height), (4, 4))
        self.assertEqual(b.blocks, {'A': 2, 'C': 1})
        self.assertEqual(b.lasers, [(2, 7, 1, -1)])
        self.assertEqual(b.targets, {(3, 0), (4, 3), (2, 5), (4, 7)})
        self.assertEqual(b.cells.count(None), 16)

    def test_fixed_and_x_cells(self):
        b = Board.from_string('GRID START\nx A\nB C\nGRID STOP\n'
                              'L 0 1 1 1\nP 1 2\n')
        self.assertIs(b.cells[0], NO_BLOCK)
        self.assertTrue(b.cells[1].fixed)
        self.assertIsInstance(b.cells[2], OpaqueBlock)

    def test_compact_rows_and_comments(self):
        b = Board.from_string('# hi\nGRID START\nooo  # row\nGRID STOP\n'
                              'A 1 # one\nL 0 1 1 1\nP 1 2\n')
        self.assertEqual(b.width, 3)

    def test_errors(self):
        bad = [
            'L 0 1 1 1\nP 1 2\n',                                   # no grid
            'GRID START\no o\nGRID STOP\nP 1 2\n',                   # no laser
            'GRID START\no o\nGRID STOP\nL 0 1 1 1\n',               # no P
            'GRID START\no o\no\nGRID STOP\nL 0 1 1 1\nP 1 2\n',     # ragged
            'GRID START\no z\nGRID STOP\nL 0 1 1 1\nP 1 2\n',        # symbol
            'GRID START\no o\nGRID STOP\nL 0 1 2 1\nP 1 2\n',        # dir
            'GRID START\no o\nGRID STOP\nL 0 1 1 1\nP 9 9\n',        # target
            'GRID START\no o\nGRID STOP\nA 3\nL 0 1 1 1\nP 1 2\n',   # too many
            'GRID START\no o\nGRID STOP\nL 0 one 1 1\nP 1 2\n',      # not int
            'GRID START\no o\nL 0 1 1 1\nP 1 2\n',                   # no STOP
            'GRID START\no o\nGRID STOP\nQ 1\nL 0 1 1 1\nP 1 2\n',   # key
        ]
        for text in bad:
            with self.assertRaises(BFFError, msg=text):
                Board.from_string(text)
