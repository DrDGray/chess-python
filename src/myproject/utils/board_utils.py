from typing import Tuple

LETTER_LOC = ["A", "B", "C", "D", "E", "F", "G", "H"]


def convert_ords_to_location(ords: Tuple[int, int]) -> Tuple[str, str]:
    return (LETTER_LOC[ords[0]], str(ords[1] + 1))


def convert_location_to_ords(location: Tuple[str, str]) -> Tuple[int, int]:
    return (LETTER_LOC.index(location[0]), int(location[1]) - 1)


NUMBER_LOC = range(1, 9)  # for the user
