from _helper import *
from typing import Tuple


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
