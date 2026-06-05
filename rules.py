from pieces import *
from player import Player


class Rules:

    # TODO: make instance and pass player objects -- make functions instance

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
                    or Rules.will_move_put_in_check(dest_move, p2)
                )

        return True
