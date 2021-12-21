import math
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Callable, Set, Dict

from utils import (
    RowCol, Cell
)

from aocd import data


test_input = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def part1(lines: List[str]):
    low_points = find_low_points(lines)

    print(f"Low points: {low_points}")
    print(f"Low points count: {len(low_points)}")
    print(f"Risk: {sum([p.val for p in low_points]) + len(low_points)}")




def part2(lines: List[str]):
    low_points = find_low_points(lines)

    visited: Set[Cell] = set()
    basins: List[Set[Cell]] = []
    # For each low point expand out
    for lp in low_points:
        basin = expand_low_point(lines, lp, visited)
        print(f"Got basin: {len(basin)} - {basin}")
        basins.append(basin)

    # get 3 biggest basins
    sizes = [len(b) for b in basins]
    sizes.sort(reverse=True)
    # Sum first 3
    top3 = sizes[:3]
    print(top3)
    print(math.prod(top3))



def expand_low_point(lines: List[str], start: Cell, visited: Set[Cell]) -> Set[Cell]:
    basin: Set[Cell] = {start}
    visited.add(start)
    to_visit = [n for n in neighbours(lines, start.pos) if not n in visited]
    while to_visit:
        next = to_visit.pop()
        visited.add(next)
        # add unless its a 9
        if next.val == 9:
            continue
        else:
            basin.add(next)
            to_visit.extend([n for n in neighbours(lines, next.pos) if not n in visited])

    return basin


def find_low_points(lines: List[str]) -> List[Cell]:
    low_points: List[Cell] = []
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            pos = RowCol(row, col)
            val = int(lines[pos.row][pos.col])
            found_lower = False
            for n in neighbours(lines, pos):
                if n.val <= val:
                    found_lower = True
                    break
            if not found_lower:
                low_points.append(Cell(val, pos))
    return low_points


def neighbours(lines: List[str], pos: RowCol) -> List[Cell]:
    for rc in pos.neighbours4():
        try:
            yield Cell(int(lines[rc.row][rc.col]), rc)
        except IndexError:
            pass


if __name__ == "__main__":
    test_lines = test_input.splitlines()
    print(test_lines[0][1])


    part1(test_lines)
    part1(data.splitlines())
    part2(test_lines)
    part2(data.splitlines())

    # 1774 too high
