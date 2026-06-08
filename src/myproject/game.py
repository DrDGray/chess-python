from .player import Player, PlayerBlack, PlayerWhite
from .rules import Rules
from .utils import *
from .pieces import *
from typing import Optional, Tuple
import re
import os


class Game:

    def __init__(self):
        self.p1 = PlayerWhite()
        self.p2 = PlayerBlack()

        self.turn = self.p1

        self.valid_move: Optional[Tuple[Tuple[str, str], Tuple[str, str]]] = None

        self.rules = Rules(self.p1, self.p2)

        self.game_over = False

    def __call__(self):
        while not self.game_over:
            self._do_turn()

    def _get_roles(self) -> Tuple[Player, Player]:
        """Returns (attacker, defender)"""
        return (self.p1, self.p2) if self.turn == self.p1 else (self.p2, self.p1)

    def _change_turn(self) -> None:
        self.turn = self.p1 if self.turn != self.p1 else self.p2

    def _do_turn(self) -> None:

        self._show_board()
        self._get_valid_move()
        self._make_valid_move()
        self._change_turn()
        self._check_game_over()

    def _show_board(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print("\t" + "\t".join(LETTER_LOC), end="\n\n")  # Cols

        for row in range(8, 0, -1):
            row = str(row)
            print(row, end="\t")
            for col in LETTER_LOC:
                if (piece := self.p1.get_piece_at_location((col, row))) is not None:
                    print(piece, end="\t")
                elif (piece := self.p2.get_piece_at_location((col, row))) is not None:
                    print(piece, end="\t")
                else:
                    print("<>", end="\t")
            print()

        print("\n\t" + "\t".join(LETTER_LOC), end="\n\n")  # Cols

    def _get_valid_move(self) -> None:

        attacker, _ = self._get_roles()

        attacker_piece_locations = attacker.get_piece_locations()  # (A, 1)

        while True:

            player_move = input('Enter move in format "B7 C6":')
            if not re.search(r"[A-Ha-h][1-8]\s[A-Ha-h][1-8](\s)?", player_move):  # type: ignore
                print("ERROR: Invalid input.", end="\n")
                continue
            move_start_location = (player_move[0].upper(), player_move[1])
            move_end_location = (player_move[3].upper(), player_move[4])

            # Invalid Choice
            if not move_start_location in attacker_piece_locations:
                print("ERROR: Invalid piece chosen.", end="\n")
                continue

            # Player Piece
            if move_end_location in attacker_piece_locations:
                print("ERROR: Cannot take own piece.", end="\n")
                continue

            # Is move in moveset for piece?
            moving_piece = attacker.get_piece_at_location(move_start_location)
            assert moving_piece is not None
            if not moving_piece.is_valid_move(move_end_location):
                print("ERROR: Illegal move for piece.", end="\n")
                continue

            # Is blocking piece en-route?
            if self.rules.is_blocking_piece_en_route(
                moving_piece, move_start_location, move_end_location
            ):
                print(
                    "ERROR: Illegal move for piece (piece blocking en-route).",
                    end="\n",
                )
                continue

            # Move requirements
            if self.rules.is_meet_move_condition(moving_piece, move_end_location):
                self.valid_move = (move_start_location, move_end_location)
                break
            else:
                print("ERROR: Move requirements not met.", end="\n")
                continue

    def _make_valid_move(self) -> None:

        assert self.valid_move is not None
        src = self.valid_move[0]
        dst = self.valid_move[1]

        attacker, defender = self._get_roles()

        moving_piece = attacker.get_piece_at_location((src[0], src[1]))
        assert moving_piece is not None
        moving_piece.set_location((dst[0], dst[1]))

        if (
            taken_piece := defender.get_piece_at_location((dst[0], dst[1]))
        ) is not None:
            defender.remove_piece(taken_piece)

        self.rules.set_player_check_status(defender)

    def _check_game_over(self) -> None:  # TODO:
        pass
