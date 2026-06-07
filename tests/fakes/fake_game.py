from collections.abc import Iterator
from src.myproject import *
import sys
from ..testutils import *


class GameTest(Game):

    def __init__(self, input_str: Iterator[str]):
        self.input: Iterator[str] = input_str  # NOTE: player moves are pre-determined
        super().__init__()

    def _show_board(self) -> None:  # NOTE: visualisation unnecessary for testing
        pass

    def _get_valid_move(self) -> None:  # NOTE: overridden to raise exceptions

        attacker, _ = self._get_roles()

        attacker_piece_locations = attacker.get_piece_locations()  # (A, 1)

        while True:

            player_move = next(self.input)
            if player_move == "q()":  # NOTE: test-specific
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
