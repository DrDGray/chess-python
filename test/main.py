from collections.abc import Iterator
import unittest, sys

from myproject.src import *

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


class InvalidMoveError(Exception):
    pass


class GameTest(Game):

    def __init__(self, input_str: Iterator[str]):
        self.input: Iterator[str] = input_str  # NOTE: player moves are pre-determined
        super().__init__()

    def _show_board(self) -> None:  # NOTE: visualisation unnecessary for testing
        pass

    def _get_valid_move(self) -> None:

        attacker, _ = self._get_roles()

        attacker_piece_locations = attacker.get_piece_locations()  # (A, 1)

        while True:

            player_move = next(self.input)
            if player_move == "q()":
                sys.exit(0)
            elif not re.search(r"[A-Ha-h][0-7]\s[A-Ha-h][0-7](\s)?", player_move):  # type: ignore
                raise InvalidMoveError()
            move_start_location = (player_move[0].upper(), player_move[1])
            move_end_location = (player_move[3].upper(), player_move[4])

            # Invalid Choice
            if not move_start_location in attacker_piece_locations:
                raise InvalidMoveError("Player piece not chosen")

            # Player Piece
            if move_end_location in attacker_piece_locations:
                raise InvalidMoveError("Cannot take own piece.")

            # Is move in moveset for piece?
            moving_piece = attacker.get_piece_at_location(move_start_location)
            assert moving_piece is not None
            if not moving_piece.is_valid_move(move_end_location):
                print("ERROR: Illegal move for piece.", end="\n")  # TODO: test
                continue

            # Is blocking piece en-route?
            if self.rules.is_blocking_piece_en_route(
                moving_piece, move_start_location, move_end_location
            ):
                print(  # TODO: test
                    "ERROR: Illegal move for piece (piece blocking en-route).",
                    end="\n",
                )
                continue

            # Move requirements
            if self.rules.is_meet_move_condition(moving_piece, move_end_location):
                self.valid_move = (move_start_location, move_end_location)
                break
            else:  # TODO: test specific requirements
                print("ERROR: Move requirements not met.", end="\n")  # TODO: test
                continue


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
