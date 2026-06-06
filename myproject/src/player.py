from abc import ABC
from enum import Enum
from typing import Optional, Tuple
from .pieces import *


class PlayerType(Enum):
    WHITE = 1
    BLACK = 2


class Player(ABC):

    def __init__(self, type: PlayerType):
        self.type = type
        self.pieces = self._setup_pieces()

        if self.type is PlayerType.BLACK:
            for piece in self.pieces:
                piece.invert_moveset()

    def _setup_pieces(self) -> list[ChessPiece]:

        return [
            *[
                Pawn(self.type, (x, y))
                for x, y in zip(
                    range(8), [1 if self.type is PlayerType.WHITE else 6] * 8
                )
            ],
            *[
                Rook(self.type, (x, y))
                for x, y in zip([0, 7], [0 if self.type is PlayerType.WHITE else 7] * 2)
            ],
            *[
                Knight(self.type, (x, y))
                for x, y in zip([1, 6], [0 if self.type is PlayerType.WHITE else 7] * 2)
            ],
            *[
                Bishop(self.type, (x, y))
                for x, y in zip([2, 5], [0 if self.type is PlayerType.WHITE else 7] * 2)
            ],
            Queen(self.type, (3, 0 if self.type is PlayerType.WHITE else 7)),
            King(self.type, (4, 0 if self.type is PlayerType.WHITE else 7)),
        ]

    def remove_piece(self, piece: ChessPiece) -> None:
        self.pieces.remove(piece)

    def get_piece_at_location(self, loc: Tuple[str, str]) -> Optional[ChessPiece]:
        for piece in self.pieces:
            if piece.get_location() == loc:
                return piece
        return None

    def get_piece_ords(self) -> list[Tuple[int, int]]:
        return [p.get_ords() for p in self.pieces]

    def get_piece_locations(self) -> list[Tuple[str, str]]:
        return [p.get_location() for p in self.pieces]

    def is_takeable_piece(self, dest: Tuple[str, str]) -> bool:
        piece = self.get_piece_at_location(dest)
        return not (piece is None or isinstance(piece, King))

    def is_piece_at_location(self, loc: Tuple) -> bool:  # TODO:
        pass


class PlayerWhite(Player):
    def __init__(self):
        super().__init__(PlayerType.WHITE)


class PlayerBlack(Player):
    def __init__(self):
        super().__init__(PlayerType.BLACK)
