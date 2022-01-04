import unittest
from typing import List, Tuple, Set

import aocd

test_input = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

from utils import RowCol

def parse(input: List[str]) -> Tuple[Set[RowCol], Set[RowCol], RowCol]:
    rights: Set[RowCol] = set()
    downs: Set[RowCol] = set()

    for r, line in enumerate(input):
        for c, s in enumerate(line):
            if s == ">":
                rights.add(RowCol(r, c))
            elif s == "v":
                downs.add(RowCol(r, c))
    return rights, downs, RowCol(len(input), len(input[0]))


def move(rights: Set[RowCol], downs: Set[RowCol], bounds: RowCol) -> Tuple[bool, Set[RowCol], Set[RowCol]]:
    next_rights: Set[RowCol] = set()
    next_downs: Set[RowCol] = set()
    moved = False
    for r in rights:
        # check if there's one to the right
        next_pos = RowCol(r.row, (r.col + 1) % bounds.col)
        if next_pos not in rights and next_pos not in downs:
            # Can move
            next_rights.add(next_pos)
            moved = True
        else:
            # can't move
            next_rights.add(r)
    # Now downs
    for d in downs:
        next_pos = RowCol((d.row+1) % bounds.row, d.col)
        if next_pos not in next_rights and next_pos not in downs:
            next_downs.add(next_pos)
            moved = True
        else:
            next_downs.add(d)
    return moved, next_rights, next_downs

def move_till_stuck(rights: Set[RowCol], downs: Set[RowCol], bounds: RowCol) -> int:

    moved = True
    count = 0
    print("Initial")
    # print_grid(rights, downs, bounds)
    while moved:
        moved, rights, downs = move(rights, downs, bounds)
        count += 1
        # print(f"Count: {count}")
        # print_grid(rights, downs, bounds)

    print(f"Count: {count}")
    return count

def print_grid(rights: Set[RowCol], downs: Set[RowCol], bounds: RowCol):
    for r in range(bounds.row):
        line = ""
        for c in range(bounds.col):
            rc = RowCol(r, c)
            line += ">" if rc in rights else "v" if rc in downs else "."
        print(line)

class TestDay25(unittest.TestCase):
    def test_parse(self):
        input = """>>
v."""
        rights, downs, bounds = parse(input.splitlines())
        self.assertEqual(2, len(rights))
        self.assertEqual(1, len(downs))
        self.assertEqual(RowCol(2,2), bounds)

    def test_part1_test(self):
        self.assertEqual(58, move_till_stuck(*parse(test_input.splitlines())))

    def test_part1(self):
        self.assertEqual(278, move_till_stuck(*parse(aocd.data.splitlines())))
