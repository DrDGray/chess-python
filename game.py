from player import Player, PlayerBlack, PlayerWhite
from rules import Rules
from typing import Tuple
from _helper import *
from pieces import *
import re
import os


class Game:

    def __init__(self):
        self.p1 = PlayerWhite()
        self.p2 = PlayerBlack()

    def __call__(self):

        while True:
            if Game.do_turn(self.p1, self.p2):
                break
            if Game.do_turn(self.p2, self.p1):
                break

    @staticmethod
    def do_turn(player: Player, enemy: Player):

        Game._show_board(player, enemy)
        player_move = Game._get_valid_move(player, enemy)
        Game._make_valid_move(player_move, player, enemy)
        return Game.is_game_over()

    @staticmethod
    def _show_board(p1: Player, p2: Player) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print("\t" + "\t".join(LETTER_LOC), end="\n\n")  # Cols

        for row in range(8, 0, -1):
            row = str(row)
            print(row, end="\t")
            for col in LETTER_LOC:
                if (piece := p1.get_piece_at_location((col, row))) is not None:
                    print(piece, end="\t")
                elif (piece := p2.get_piece_at_location((col, row))) is not None:
                    print(piece, end="\t")
                else:
                    print("<>", end="\t")
            print()

        print("\n\t" + "\t".join(LETTER_LOC), end="\n\n")  # Cols

    @staticmethod
    def _get_valid_move(
        p1: Player, p2: Player
    ) -> Tuple[Tuple[str, str], Tuple[str, str]]:

        p1_piece_locations = p1.get_piece_locations()  # (A, 1)

        while True:

            player_move = input('Enter move in format "B7 C6":')
            if not re.search(r"[A-Ha-h][0-7]\s[A-Ha-h][0-7](\s)?", player_move):  # type: ignore
                continue
            move_start_location = (player_move[0].upper(), player_move[1])
            move_end_location = (player_move[3].upper(), player_move[4])

            # Invalid Choice
            if not move_start_location in p1_piece_locations:
                print("ERROR: Invalid piece chosen.", end="\n")
                continue

            # On the board?
            if not (
                move_end_location[0] in LETTER_LOC
                and int(move_end_location[1]) in NUMBER_LOC
            ):
                print("ERROR: Move location not on board.", end="\n")
                continue

            # Player Piece
            if move_end_location in p1_piece_locations:
                print("ERROR: Cannot take own piece.", end="\n")
                continue

            # Is move in moveset for piece?
            moving_piece = p1.get_piece_at_location(move_start_location)
            assert moving_piece is not None
            if not moving_piece.is_valid_move(move_end_location):
                print("ERROR: Illegal move for piece.", end="\n")
                continue

            # Is blocking piece en-route?
            if Rules.is_blocking_piece_en_route(
                moving_piece, move_start_location, move_end_location, p1, p2
            ):
                print(
                    "ERROR: Illegal move for piece (piece blocking en-route).",
                    end="\n",
                )
                continue

            # Move requirements
            if Rules.is_meet_move_condition(moving_piece, move_end_location, p2):
                return (move_start_location, move_end_location)
            else:
                print("ERROR: Move requirements not met.", end="\n")
                continue

    @staticmethod
    def _make_valid_move(
        move: Tuple[Tuple[str, str], Tuple[str, str]], p1: Player, p2: Player
    ):
        src = move[0]
        dst = move[1]

        moving_piece = p1.get_piece_at_location(src)
        assert moving_piece is not None
        moving_piece.set_location(dst)

        if (taken_piece := p2.get_piece_at_location(dst)) is not None:
            p2.remove_piece(taken_piece)

    @staticmethod
    def is_game_over() -> bool:  # TODO:
        return False
