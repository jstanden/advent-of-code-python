import math

NESW = ((-1, 0), (0, 1), (1, 0), (0, -1))
NESW_DIAG = ((-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (-1, -1), (1, -1), (1, 1))

SWNE = ((1, 0), (0, -1), (-1, 0), (0, 1))


def add(v1, v2):
    return tuple([v1[n] + v2[n] for n in range(len(v1))])


def mul(v1, factor: int):
    return [v1[i] * factor for i in range(len(v1))]


def rotate(from_heading: tuple, side: str) -> tuple:
    return (-from_heading[1], from_heading[0]) \
        if 'L' == side else (from_heading[1], -from_heading[0])


def invert(v1: tuple) -> tuple:
    return -v1[0], -v1[1]


def north(v: tuple) -> tuple:
    return add(v, NESW[0])


def east(v: tuple) -> tuple:
    return add(v, NESW[1])


def south(v: tuple) -> tuple:
    return add(v, NESW[2])


def west(v: tuple) -> tuple:
    return add(v, NESW[3])


def slope(v1, v2):
    return v2[0] - v1[0], v2[1] - v1[1]


def dist_euclid(v1, v2) -> float:
    return math.sqrt(math.pow(v2[1] - v1[1], 2) + math.pow(v2[0] - v1[0], 2))


def dist_manhattan(v1, v2) -> int:
    return abs(v1[1] - v2[1]) + abs(v1[0] - v2[0])