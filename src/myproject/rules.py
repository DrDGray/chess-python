from .pieces import *
from .player import Player
from typing import Optional


class Rules:

    # TODO: implement checkmate

    def __init__(self, p1: Player, p2: Player) -> None:
        self.p1 = p1
        self.p2 = p2
        self.blocking_piece: Optional[ChessPiece] = None

    def is_blocking_piece_en_route(
        self,
        moving_piece: ChessPiece,
        move_start_location: tuple[str, str],
        move_end_location: tuple[str, str],
        *,
        is_computing_check: bool = False,
    ) -> bool:
        """Checks for blocking piece on route to destination and returns
        the appropriate boolean value. The blocking piece is stored in
        self.blocking_piece."""

        if not is_computing_check:
            if not any(isinstance(moving_piece, x) for x in [Bishop, Queen, Rook]):
                return False

        start_ords = convert_location_to_ords(
            (move_start_location[0], move_start_location[1])
        )
        end_ords = convert_location_to_ords(
            (move_end_location[0], move_end_location[1])
        )
        board_piece_ords = self.p1.get_piece_ords() + self.p2.get_piece_ords()

        def is_piece_at_location(ords: Tuple[int, int]) -> bool:
            if ords in board_piece_ords:
                if (cur_piece := self.p1.get_piece_at_ords(ords)) is not None:
                    self.blocking_piece = cur_piece
                else:
                    self.blocking_piece = self.p2.get_piece_at_ords(ords)
                return True
            return False

        def check_horizontals() -> bool:

            # Horizontal right
            if start_ords[0] < end_ords[0] and start_ords[1] == end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] + 1, end_ords[0]),
                    [start_ords[1]] * (end_ords[0] - start_ords[0] - 1),
                ):
                    if is_piece_at_location((x, y)):
                        return True

            # Horizontal left
            if start_ords[0] > end_ords[0] and start_ords[1] == end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] - 1, end_ords[0], -1),
                    [start_ords[1]] * (end_ords[0] - start_ords[0] - 1),
                ):
                    if is_piece_at_location((x, y)):
                        return True

            return False

        def check_verticals() -> bool:

            # Vertical up
            if start_ords[0] == end_ords[0] and start_ords[1] < end_ords[1]:
                for x, y in zip(
                    [start_ords[0]] * (end_ords[1] - start_ords[1] - 1),
                    range(start_ords[1] + 1, end_ords[1]),
                ):
                    if is_piece_at_location((x, y)):
                        return True

            # Vertical down
            if start_ords[0] == end_ords[0] and start_ords[1] > end_ords[1]:
                for x, y in zip(
                    [start_ords[0]] * (start_ords[1] - end_ords[1] - 1),
                    range(start_ords[1] - 1, end_ords[1], -1),
                ):
                    if is_piece_at_location((x, y)):
                        return True

            return False

        def check_diagonals() -> bool:

            # Diagonal up right
            if start_ords[0] < end_ords[0] and start_ords[1] < end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] + 1, end_ords[0]),
                    range(start_ords[1] + 1, end_ords[1]),
                ):
                    if is_piece_at_location((x, y)):
                        return True

            # Diagonal up left
            if start_ords[0] > end_ords[0] and start_ords[1] < end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] - 1, end_ords[0], -1),
                    range(start_ords[1] + 1, end_ords[1]),
                ):
                    if is_piece_at_location((x, y)):
                        return True

            # Diagonal down right
            if start_ords[0] < end_ords[0] and start_ords[1] > end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] + 1, end_ords[0]),
                    range(start_ords[1] - 1, end_ords[1], -1),
                ):
                    if is_piece_at_location((x, y)):
                        return True

            # Diagonal down left
            if start_ords[0] > end_ords[0] and start_ords[1] > end_ords[1]:
                for x, y in zip(
                    range(start_ords[0] - 1, end_ords[0], -1),
                    range(start_ords[1] - 1, end_ords[1], -1),
                ):
                    if is_piece_at_location((x, y)):
                        return True

            return False

        if is_computing_check:
            return check_diagonals() or check_horizontals() or check_verticals()

        if isinstance(moving_piece, Rook):
            return check_horizontals() or check_verticals()
        elif isinstance(moving_piece, Bishop):
            return check_diagonals()
        elif isinstance(moving_piece, Queen):
            return check_horizontals() or check_verticals() or check_diagonals()

        return False

    def _will_move_put_in_check(self, dest: Tuple[str, str]) -> bool:  # TODO:
        return False

    def is_piece_being_attacked(
        self, *, defending_piece: ChessPiece, attacking_piece: ChessPiece
    ) -> bool:

        if attacking_piece.owner == defending_piece.owner:
            return False

        defending_piece_ords = defending_piece.get_ords()
        attacker = self.p1 if attacking_piece.owner == self.p1.type else self.p2

        if any(
            defending_piece_ords == attacking_piece.compute_dest_ord(legal_move)
            and not legal_move.no_take
            for legal_move in attacking_piece.get_move_list()
        ):
            defending_piece.put_piece_in_check()
            return True

        if any(
            defending_piece_ords == knight.compute_dest_ords()
            for knight in attacker.get_knights()
        ):
            defending_piece.put_piece_in_check()
            return True

        return False

    def set_player_check_status(self, player: Player) -> bool:
        """Starts from a given chess piece and branches outwards until it meets a piece.
        If the king location is in the legal moves of that piece, the king is in check.
        Special case needed for knights.

        Returns True of there's a check and False if no check.
        """

        king_piece = player.get_king()

        king_ords = king_piece.get_ords()

        # Horizontals
        for inverter in range(-1, 2, 2):
            for x in range(1 * inverter, 8 * inverter, 1 * inverter):

                new_ord = king_ords[0] + x
                if new_ord > 7 or new_ord < 0:
                    break

                if self.is_blocking_piece_en_route(
                    king_piece,
                    king_piece.get_location(),
                    convert_ords_to_location((king_ords[0] + x, king_ords[1])),
                    is_computing_check=True,
                ):
                    assert self.blocking_piece is not None
                    if self.is_piece_being_attacked(
                        defending_piece=king_piece, attacking_piece=self.blocking_piece
                    ):
                        return True

        # Verticals
        for inverter in range(-1, 2, 2):
            for y in range(1 * inverter, 8 * inverter, 1 * inverter):

                new_ord = king_ords[1] + y
                if new_ord > 7 or new_ord < 0:
                    break

                if self.is_blocking_piece_en_route(
                    king_piece,
                    king_piece.get_location(),
                    convert_ords_to_location((king_ords[0], king_ords[1] + y)),
                    is_computing_check=True,
                ):
                    assert self.blocking_piece is not None
                    if self.is_piece_being_attacked(
                        defending_piece=king_piece, attacking_piece=self.blocking_piece
                    ):
                        return True

        # Diagonals
        for inverter in range(-1, 2, 2):
            for xy in range(1 * inverter, 8 * inverter, 1 * inverter):

                new_ord_1 = king_ords[0] + xy
                new_ord_2 = king_ords[1] + xy
                if not any(ord > 7 or ord < 0 for ord in (new_ord_1, new_ord_2)):
                    if self.is_blocking_piece_en_route(  # TR BL
                        king_piece,
                        king_piece.get_location(),
                        convert_ords_to_location(
                            (king_ords[0] + xy, king_ords[1] + xy)
                        ),
                        is_computing_check=True,
                    ):
                        assert self.blocking_piece is not None
                        if self.is_piece_being_attacked(
                            defending_piece=king_piece,
                            attacking_piece=self.blocking_piece,
                        ):
                            return True

                new_ord_1 = king_ords[0] - xy
                new_ord_2 = king_ords[1] + xy
                if not any(ord > 7 or ord < 0 for ord in (new_ord_1, new_ord_2)):
                    if self.is_blocking_piece_en_route(  # TL BR
                        king_piece,
                        king_piece.get_location(),
                        convert_ords_to_location(
                            (king_ords[0] - xy, king_ords[1] + xy)
                        ),
                        is_computing_check=True,
                    ):
                        assert self.blocking_piece is not None
                        if self.is_piece_being_attacked(
                            defending_piece=king_piece,
                            attacking_piece=self.blocking_piece,
                        ):
                            return True

        return False

    def is_meet_move_condition(
        self, moving_piece: ChessPiece, dest_move: Tuple[str, str]
    ) -> bool:

        defender = self.p1 if moving_piece.owner == self.p2.type else self.p2

        move_schemas = moving_piece.get_move_list()
        for move_schema in move_schemas:

            # Find corresponding schema
            move_schema_ords = move_schema.get_ords()
            piece_ords = moving_piece.get_ords()
            dest_ords = (
                move_schema_ords[0] + piece_ords[0],
                move_schema_ords[1] + piece_ords[1],
            )

            # Boundary check
            if any(ord > 7 or ord < 0 for ord in (dest_ords[0], dest_ords[1] + 1)):
                continue

            replicated_dest_move = (LETTER_LOC[dest_ords[0]], str(dest_ords[1] + 1))
            if dest_move != replicated_dest_move:
                continue

            if move_schema.no_take and move_schema.first_move_only:
                return (
                    defender.get_piece_at_location(dest_move) is None
                    and not moving_piece.has_moved
                )
            elif move_schema.no_take:
                return defender.get_piece_at_location(dest_move) is None
            elif move_schema.first_move_only:
                return not moving_piece.has_moved
            elif move_schema.must_take:
                return defender.is_takeable_piece(dest_move)
            elif move_schema.req_no_check:
                return not (
                    moving_piece.is_in_check or self._will_move_put_in_check(dest_move)
                )

        return True
