import math
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from statistics import median
from typing import List, Callable, Set, Dict, Optional

from utils import extractInts, RowCol
from aocd import data

test_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

test_mini = """11111
19991
19191
19991
11111"""

def tick(grid: List[List[int]]) -> int:
    flashed: Set[RowCol] = set()
    to_flash: List[RowCol] = []

    # Step 1 all increase by 1
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            grid[r][c] += 1
            if grid[r][c] > 9:
                to_flash.append(RowCol(r, c))
    # Step 2 - flash and increase neighbours, checking for more flashes
    while to_flash:
        rc: RowCol = to_flash.pop(0)
        if rc in flashed:
            # Already flashed
            continue
        else:
            # increase all neighbours by 1, check for flash candidates
            flashed.add(rc)
            for n in rc.neighbours8():
                try:
                    grid[n.row][n.col] += 1
                    if grid[n.row][n.col] > 9 and n not in flashed:
                        to_flash.append(n)
                except IndexError:
                    pass
    # Step 3 set all flashed to 0
    for rc in flashed:
        grid[rc.row][rc.col] = 0

    return len(flashed)


def part1(lines: List[str], ticks=100, print_interval=1):
    grid = to_grid(lines)
    flash_count = 0
    print("Before any steps: ")
    print_grid(grid)
    for i in range(1, ticks+1):
        f = tick(grid)
        print(f"Step {i} Flashed: {f}")
        flash_count += f
        if i % print_interval == 0:
            print(f"After {i} steps: ")
            print_grid(grid)

    print(f"Total flashes {flash_count}")


def part2(lines: List[str], print_interval=1):
    grid = to_grid(lines)
    flash_target = len(lines) * len(lines[0])
    max_flash = 0
    print("Before any steps: ")
    print_grid(grid)
    step_count = 0
    while True:
        f = tick(grid)
        step_count += 1
        print(f"Step {step_count} Flashed: {f}")
        if f > max_flash:
            max_flash = f
            print(f"New max_flash of {f} after {step_count}")
        if f == flash_target:
            print(f"Flash target of {flash_target} reached after {step_count}")
            break
        if step_count % print_interval == 0:
            print(f"After {step_count} steps: ")
            print_grid(grid)



def to_grid(lines: List[str]) -> List[List[int]]:
    return [[int(c) for c in line] for line in lines]


def print_grid(grid: List[List[int]]):
    for r in range(len(grid)):
        print("".join([str(i) for i in grid[r]]))


if __name__ == "__main__":
    test_lines = test_input.splitlines()

    part1(test_lines, 100, 10)
    part1(data.splitlines(), 100, 1000)
    part2(test_lines)
    part2(data.splitlines())
