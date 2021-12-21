from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from typing import List, Callable, Set, Dict, Optional, Tuple

from utils import extractInts, RowCol, Coord
from aocd import data



test_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

def parse(lines: List[str]) -> Tuple[Set[Coord], List[str]]:
    points: Set[Coord] = set()
    instructions: List[str] = []

    for line in lines:
        if line:
            if line.startswith("fold"):
                instructions.append(line)
            else:
                nums = extractInts(line)
                points.add(Coord(nums[0], nums[1]))

    return points, instructions,



def part1(lines: List[str]):
    points, instructions = parse(lines)
    print(f"There are {len(points)}")
    # Now we've parsed, apply the first instruction
    result = apply(instructions[0], points)
    print(f"There are now {len(result)}")

def part2(lines: List[str]):
    points, instructions = parse(lines)
    for i in instructions:
        points = apply(i, points)
    print(f"There are now {len(points)}")
    # now print it
    print_grid(points)


def print_grid(points: Set[Coord]):
    max_x = max([p.x for p in points]) +1
    max_y = max([p.y for p in points]) +1
    grid : List[List[str]] = []
    for i in range(max_y):
        grid.append(["."] * max_x)
    for g in grid:
        print("".join(g))

    for p in points:
        grid[p.y][p.x] = "#"

    for g in grid:
        print("".join(g))

def apply(instruction: str, points: Set[Coord]) -> Set[Coord]:
    return fold(points, "x" in instruction, extractInts(instruction)[0])


def fold(points: Set[Coord], xfold: bool, val: int) -> Set[Coord]:
    result: Set[Coord] = set()

    for p in points:
        if xfold:
            if p.x <= val:
                result.add(p)
            else:
                diff = p.x - val
                new_x = val - diff
                coord = Coord(new_x, p.y)
                if coord in result:
                    print(f"Found a merge: {coord} was {p}")
                result.add(coord)
        else:
            if p.y <= val:
                result.add(p)
            else:
                diff = p.y - val
                new_y = val - diff
                coord = Coord(p.x, new_y)
                if coord in result:
                    print(f"Found a merge: {coord} was {p}")
                result.add(coord)
    return result

if __name__ == "__main__":
    # part1(test_input.splitlines())
    # part1(data.splitlines())
    part2(test_input.splitlines())
    part2(data.splitlines())