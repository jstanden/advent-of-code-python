from typing import Callable, List
from collections import defaultdict
import lib.aoc.grid2d.vector as vector2d


def parse(data: str, as_int: bool = False) -> (defaultdict, dict):
    return defaultdict(None, {(y, x): int(symbol) if as_int else symbol
                       for y, row in enumerate(data.splitlines())
                       for x, symbol in enumerate(list(row))})


def render(top_left: tuple, bottom_right: tuple, func: Callable) -> None:
    for y in range(top_left[0], bottom_right[0]):
        for x in range(top_left[1], bottom_right[1]):
            func((y,x))
        print("")


def find_coords(grid: defaultdict, value):
    return set([yx for yx, _ in filter(lambda item: item[1] == value, grid.items())])


def neighbors(grid: defaultdict, at: tuple, directions: List[tuple]):
    results = []
    for d in directions:
        n_at = vector2d.add(at, d)
        if grid.get(n_at):
            results.append((n_at, grid[n_at]))
    return results


def fill(top_left: tuple, bot_right: tuple) -> list:
    x_delta = 1 if bot_right[1] > top_left[1] else -1
    y_delta = 1 if bot_right[0] > top_left[0] else -1
    return list([(y, x)
                for y in range(top_left[0], bot_right[0] + y_delta, y_delta)
                for x in range(top_left[1], bot_right[1] + x_delta, x_delta)])

