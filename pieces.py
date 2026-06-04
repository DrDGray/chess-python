from __future__ import annotations

from abc import abstractmethod
from typing import Tuple

LETTER_LOC = ["A", "B", "C", "D", "E", "F", "G", "H"]


class ChessMove:
    def __init__(
        self,
        x_axis: int,
        y_axis: int,
        *,
        must_take: bool = False,
        req_no_check: bool = False,
        first_move_only: bool = False,
        no_take: bool = False
    ):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.must_take = must_take
        self.req_no_check = req_no_check
        self.first_move_only = first_move_only
        self.no_take = no_take

    def invert_moveset(self) -> None:
        self.x_axis = -self.x_axis
        self.y_axis = -self.y_axis

    def get_loc(self) -> Tuple[str, str]:
        return (LETTER_LOC[self.x_axis], str(self.y_axis))

    def get_ords(self) -> Tuple[int, int]:
        return (self.x_axis, self.y_axis)

    @staticmethod
    def is_blocking_piece_en_route(
        moving_piece: ChessPiece,
        move_start_location: tuple[str, str],
        move_end_location: tuple[str, str],
        p1: Player,
        p2: Player,
    ) -> bool:

        if not any(isinstance(moving_piece, x) for x in [Bishop, Queen, Rook]):
            return False

        start_ords = (
            LETTER_LOC.index(move_start_location[0]),
            int(move_start_location[1]) - 1,
        )
        end_ords = (
            LETTER_LOC.index(move_end_location[0]),
            int(move_end_location[1]) - 1,
        )
        board_piece_ords = p1.get_piece_ords() + p2.get_piece_ords()

        def check_horizontals() -> bool:

            # Horizontal right
            if start_ords[0] < end_ords[0] and start_ords[1] == end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] + 1, end_ords[0]),
                    [start_ords[1]] * (end_ords[0] - start_ords[0] - 1),
                ):
                    if (x, y) in board_piece_ords:
                        return True

            # Horizontal left
            if start_ords[0] > end_ords[0] and start_ords[1] == end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] - 1, end_ords[0], -1),
                    [start_ords[1]] * (end_ords[0] - start_ords[0] - 1),
                ):
                    if (x, y) in board_piece_ords:
                        return True

            return False

        def check_verticals() -> bool:

            # Vertical up
            if start_ords[0] == end_ords[0] and start_ords[1] < end_ords[1]:
                for x, y in zip(
                    [start_ords[0]] * (end_ords[1] - start_ords[1] - 1),
                    range(start_ords[1] + 1, end_ords[1]),
                ):
                    if (x, y) in board_piece_ords:
                        return True

            # Vertical down
            if start_ords[0] == end_ords[0] and start_ords[1] > end_ords[1]:
                for x, y in zip(
                    [start_ords[0]] * (start_ords[1] - end_ords[1] - 1),
                    range(start_ords[1] - 1, end_ords[1], -1),
                ):
                    if (x, y) in board_piece_ords:
                        return True

            return False

        def check_diagonals() -> bool:

            # Diagonal up right
            if start_ords[0] < end_ords[0] and start_ords[1] < end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] + 1, end_ords[0]),
                    range(start_ords[1] + 1, end_ords[1]),
                ):
                    if (x, y) in board_piece_ords:
                        return True

            # Diagonal up left
            if start_ords[0] > end_ords[0] and start_ords[1] < end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] - 1, end_ords[0], -1),
                    range(start_ords[1] + 1, end_ords[1]),
                ):
                    if (x, y) in board_piece_ords:
                        return True

            # Diagonal down right
            if start_ords[0] < end_ords[0] and start_ords[1] > end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] + 1, end_ords[0]),
                    range(start_ords[1] - 1, end_ords[1], -1),
                ):
                    if (x, y) in board_piece_ords:
                        return True

            # Diagonal down left
            if start_ords[0] > end_ords[0] and start_ords[1] > end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] - 1, end_ords[0], -1),
                    range(start_ords[1] - 1, end_ords[1], -1),
                ):
                    if (x, y) in board_piece_ords:
                        return True

            return False

        if isinstance(moving_piece, Rook):
            return check_horizontals() or check_verticals()
        elif isinstance(moving_piece, Bishop):
            return check_diagonals()
        elif isinstance(moving_piece, Queen):
            return check_horizontals() or check_verticals() or check_diagonals()

        return False

    @staticmethod
    def will_move_put_in_check(dest: Tuple[str, str], p2: Player) -> bool:  # TODO:
        return False

    @staticmethod
    def is_meet_move_condition(
        moving_piece: ChessPiece, dest_move: Tuple[str, str], p2: Player
    ) -> bool:

        move_schemas = moving_piece.get_move_list()
        for move_schema in move_schemas:

            # Find corresponding schema
            move_schema_ords = move_schema.get_ords()
            piece_ords = moving_piece.get_ords()
            dest_ords = (
                move_schema_ords[0] + piece_ords[0],
                move_schema_ords[1] + piece_ords[1],
            )
            replicated_dest_move = (LETTER_LOC[dest_ords[0]], str(dest_ords[1] + 1))
            if dest_move != replicated_dest_move:
                continue

            if move_schema.no_take and move_schema.first_move_only:
                return (
                    p2.get_piece_at_location(dest_move) is None
                    and not moving_piece.has_moved
                )
            elif move_schema.no_take:
                return p2.get_piece_at_location(dest_move) is None
            elif move_schema.first_move_only:
                return not moving_piece.has_moved
            elif move_schema.must_take:
                return p2.is_takeable_piece(dest_move)
            elif move_schema.req_no_check:
                return not (
                    moving_piece.is_in_check
                    or ChessMove.will_move_put_in_check(dest_move, p2)
                )

        return True

class ChessPiece:

    @abstractmethod
    def __init__(
        self, owner: PlayerType, ords: Tuple[int, int], move_list: list[ChessMove]
    ):

        self.owner = owner
        self.ords = ords
        self.move_list = move_list

        self.has_moved = False
        self.is_in_check = False

    def invert_moveset(self) -> None:
        for move in self.move_list:
            move.invert_moveset()

    def _get_row_ord(self) -> int:
        return self.ords[1]

    def _get_col_ord(self) -> int:
        return self.ords[0]

    def get_move_list(self) -> list[ChessMove]:
        return self.move_list

    def get_ords(self) -> Tuple[int, int]:
        return (self.ords[0], self.ords[1])

    def get_location(self) -> Tuple[str, str]:
        return (LETTER_LOC[self._get_col_ord()], str(self._get_row_ord() + 1))

    def set_location(self, location: Tuple[str, str]) -> None:
        self.ords = [LETTER_LOC.index(location[0]), int(location[1]) - 1]
        self.has_moved = True

    def compute_dest_ords(self) -> list[Tuple[int, int]]:
        return [
            (move.x_axis + self.ords[0], move.y_axis + self.ords[1])
            for move in self.move_list
        ]

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("Implement __str__() for chess piece")

    def compute_dest_locs(self) -> list[Tuple[str, str]]:
        """Returns a list of locations according to move rules.
        The validity of the rules must be verified.
        """
        return [
            (
                LETTER_LOC[move.x_axis + self.ords[0]],
                str(move.y_axis + self.ords[1] + 1),
            )
            for move in self.move_list
            if (move.x_axis + self.ords[0] < 8 and move.y_axis + self.ords[1] + 1 < 8)
        ]

    def is_valid_move(self, dest: Tuple[str, str]) -> bool:
        """Returns if dest is a hypothetically valid move for piece."""
        return dest in self.compute_dest_locs()

class Pawn(ChessPiece):

    # TODO: en passant

    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        move_list = [
            ChessMove(0, 1, no_take=True),
            ChessMove(0, 2, first_move_only=True, no_take=True),
            ChessMove(1, 1, must_take=True),
            ChessMove(-1, 1, must_take=True),
        ]
        super().__init__(owner, ords, move_list)

    def __str__(self) -> str:
        return "P"


class Knight(ChessPiece):

    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        move_list = [
            ChessMove(1, 2),
            ChessMove(-1, 2),
            ChessMove(1, -2),
            ChessMove(-1, -2),
        ]
        super().__init__(owner, ords, move_list)

    def __str__(self) -> str:
        return "KN"


DIAGONAL_MOVES = [
    *[ChessMove(x, y) for x, y in zip(range(1, 7), range(1, 7))],  # Up right
    *[ChessMove(x, y) for x, y in zip(range(-1, -7, -1), range(1, 7))],  # Up left
    *[ChessMove(x, y) for x, y in zip(range(1, 7), range(-1, -7, -1))],  # Down right
    *[
        ChessMove(x, y) for x, y in zip(range(-1, -7, -1), range(-1, -7, -1))
    ],  # Down left
]


class Bishop(ChessPiece):

    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        super().__init__(owner, ords, DIAGONAL_MOVES)

    def __str__(self) -> str:
        return "B"


HORIZONTAL_MOVES = [
    *[ChessMove(x, y) for x, y in zip([0] * 7, range(1, 7))],  # Up
    *[ChessMove(x, y) for x, y in zip([0] * 7, range(-1, -7, -1))],  # Down
    *[ChessMove(x, y) for x, y in zip(range(1, 7), [0] * 7)],  # Right
    *[ChessMove(x, y) for x, y in zip(range(-1, -7, -1), [0] * 7)],  # Left
]
class Rook(ChessPiece):


    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        super().__init__(owner, ords, HORIZONTAL_MOVES)

    def __str__(self) -> str:
        return "R"


class Queen(ChessPiece):

    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        super().__init__(owner, ords, DIAGONAL_MOVES + HORIZONTAL_MOVES)

    def __str__(self) -> str:
        return "Q"


class King(ChessPiece):

    # TODO: castle
    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        move_list = [
            *[
                ChessMove(x, y, req_no_check=True) for x, y in zip(range(-1, 2), [1] * 3)
            ],  # Top
            *[
                ChessMove(x, y, req_no_check=True) for x, y in zip(range(-1, 2), [0] * 3)
            ],  # Bottom
            *[
                ChessMove(x, y, req_no_check=True) for x, y in zip([-1, 1], [0] * 2)
            ],  # Sides
        ]
        super().__init__(owner, ords, move_list)

    def __str__(self) -> str:
        return "K"
