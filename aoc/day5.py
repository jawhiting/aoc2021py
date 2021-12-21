import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List

INT_PATTERN = re.compile("(-?[0-9]+)")

def extractInts(s: str) -> List[int]:
    return [int(n) for n in re.findall(INT_PATTERN, s)]

test_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int

def part1(lines: List[str], horizontal_only=True):
    visit_count = defaultdict(int)

    for l in lines:
        ints = extractInts(l)
        f = Point(ints[0], ints[1])
        t = Point(ints[2], ints[3])
        # Iterate from f to t
        x_inc = 0 if t.x == f.x else (t.x-f.x) / abs(t.x-f.x)
        y_inc = 0 if t.y == f.y else (t.y-f.y) / abs(t.y-f.y)
        if x_inc == 0 and y_inc == 0:
            raise ValueError("Same point")

        # Part1 horizontal only
        if not horizontal_only or (x_inc == 0 or y_inc == 0):
            cur = Point(f.x, f.y)
            while cur != t:
                visit_count[cur] += 1
                cur = Point(cur.x + x_inc, cur.y + y_inc)
            # Mark f as well
            visit_count[t] += 1

    print(visit_count)

    intersections = sum([1 for p, c in visit_count.items() if c > 1])
    print(intersections)
    for y in range(0, 10):
        line = ""
        for x in range(0, 10):
            vc = visit_count[Point(x, y)]
            line += "." if vc == 0 else str(vc)
        print(line)



part1(test_input.splitlines())
part1(test_input.splitlines(), horizontal_only=False)
# real one
lines = [l.strip() for l in Path("day5.txt").read_text().splitlines()]
part1(lines)
part1(lines, horizontal_only=False)
