from __future__ import annotations

from abc import abstractmethod
from typing import Tuple, TYPE_CHECKING
from .utils import *
import copy

if TYPE_CHECKING:
    from .player import PlayerType


class ChessMove:

    def __init__(
        self,
        x_axis: int,
        y_axis: int,
        *,
        must_take: bool = False,
        req_no_check: bool = False,
        first_move_only: bool = False,
        no_take: bool = False,
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


HORIZONTAL_MOVES = [
    *[ChessMove(x, y) for x, y in zip([0] * 7, range(1, 7))],  # Up
    *[ChessMove(x, y) for x, y in zip([0] * 7, range(-1, -7, -1))],  # Down
    *[ChessMove(x, y) for x, y in zip(range(1, 7), [0] * 7)],  # Right
    *[ChessMove(x, y) for x, y in zip(range(-1, -7, -1), [0] * 7)],  # Left
]


DIAGONAL_MOVES = [
    *[ChessMove(x, y) for x, y in zip(range(1, 7), range(1, 7))],  # Up right
    *[ChessMove(x, y) for x, y in zip(range(-1, -7, -1), range(1, 7))],  # Up left
    *[ChessMove(x, y) for x, y in zip(range(1, 7), range(-1, -7, -1))],  # Down right
    *[
        ChessMove(x, y) for x, y in zip(range(-1, -7, -1), range(-1, -7, -1))
    ],  # Down left
]


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

    def compute_dest_ord(self, move: ChessMove) -> Tuple[int, int]:
        return (move.x_axis + self.ords[0], move.y_axis + self.ords[1])

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

    def put_piece_in_check(self) -> None:
        self.is_in_check = True

    def remove_check(self) -> None:
        self.is_in_check = False


class Pawn(ChessPiece):

    # TODO: en passant
    # TODO: promotion

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
            ChessMove(2, 1),
            ChessMove(2, -1),
            ChessMove(-2, 1),
            ChessMove(-2, -1),
        ]
        super().__init__(owner, ords, move_list)

    def __str__(self) -> str:
        return "KN"


class Bishop(ChessPiece):

    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        super().__init__(owner, ords, copy.deepcopy(DIAGONAL_MOVES))

    def __str__(self) -> str:
        return "B"


class Rook(ChessPiece):

    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        super().__init__(owner, ords, copy.deepcopy(HORIZONTAL_MOVES))

    def __str__(self) -> str:
        return "R"


class Queen(ChessPiece):

    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        super().__init__(owner, ords, copy.deepcopy(DIAGONAL_MOVES + HORIZONTAL_MOVES))

    def __str__(self) -> str:
        return "Q"


class King(ChessPiece):

    # TODO: castle
    def __init__(self, owner: PlayerType, ords: Tuple[int, int]):
        move_list = [
            *[
                ChessMove(x, y, req_no_check=True)
                for x, y in zip(range(-1, 2), [1] * 3)
            ],  # Top
            *[
                ChessMove(x, y, req_no_check=True)
                for x, y in zip(range(-1, 2), [0] * 3)
            ],  # Bottom
            *[
                ChessMove(x, y, req_no_check=True) for x, y in zip([-1, 1], [0] * 2)
            ],  # Sides
        ]
        super().__init__(owner, ords, move_list)

    def __str__(self) -> str:
        return "K"
