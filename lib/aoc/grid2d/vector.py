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


def slope(v1, v2):
    return v2[0] - v1[0], v2[1] - v1[1]