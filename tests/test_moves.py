import unittest

from .testutils import *
from .fakes.fake_game import *

"""
| Assertion              | Purpose              |
| ---------------------- | -------------------- |
| `assertEqual(a, b)`    | `a == b`             |
| `assertNotEqual(a, b)` | `a != b`             |
| `assertTrue(x)`        | `bool(x)` is `True`  |
| `assertFalse(x)`       | `bool(x)` is `False` |
| `assertIs(a, b)`       | Same object (`is`)   |
| `assertIsNot(a, b)`    | Different objects    |
| `assertIsNone(x)`      | `x is None`          |
| `assertIsNotNone(x)`   | `x is not None`      |
| `assertIn(a, b)`       | `a in b`             |
| `assertNotIn(a, b)`    | `a not in b`         |
| `assertRaises(exc)`    | Exception is raised  |
"""


class TestClass(unittest.TestCase):

    def test_p1_takes_p2_piece(self):

        input = iter(
            [
                "a2 a4",
                "b7 b5",
                "a4 b5",
                "q()",
            ]
        )

        with self.assertRaises(SystemExit) as r:
            GameTest(input)()
        self.assertEqual(r.exception.code, 0)

    def test_p1_moves_p2_piece(self):
        input = iter(
            [
                "b7 b5",
                "q()",
            ]
        )

        with self.assertRaises(InvalidMoveError) as r:
            GameTest(input)()
        self.assertEqual(str(r.exception), "Player piece not chosen")

    def test_p1_takes_own_piece(self):

        input = iter(
            [
                "a2 a3",
                "b7 b5",
                "b2 a3",
                "q()",
            ]
        )

        with self.assertRaises(InvalidMoveError) as r:
            GameTest(input)()
        self.assertEqual(str(r.exception), "Cannot take own piece.")

    def test_put_king_in_check(self):
        input = iter(
            [
                "e2 e4",
                "e7 e5",
                "d1 h5",
                "g8 f6",
                "h5 e5",  # Queen checks king along the e-file
                "q()",
            ]
        )
        self.assertTrue(False)

    def test_checkmate(self):

        input = iter(
            [
                "e2 e4",
                "e7 e5",
                "d1 h5",
                "b8 c6",
                "f1 c4",
                "g8 f6",
                "h5 f7",
                "q()",
            ]
        )
        self.assertTrue(False)

    def test_move_other_piece_when_king_in_check(self):

        input = iter(
            [
                "e2 e4",
                "e7 e5",
                "d1 h5",
                "g8 f6",
                "h5 e5",  # Queen checks king along the e-file
                "a7 a6",  # Attempt to ignore check
                "q()",
            ]
        )
        self.assertTrue(False)
