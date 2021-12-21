import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Iterator, Set, Dict

from aocd import data

from aoc import utils

test_input = "target area: x=20..30, y=-10..-5"

test_expected = """23,-10
25,-7
8,0
26,-10
20,-8
25,-6
25,-10
8,1
24,-10
7,5
23,-5
27,-10
8,-2
25,-9
26,-6
30,-6
7,-1
13,-2
15,-4
7,8
22,-8
23,-8
23,-6
24,-8
7,2
27,-8
27,-5
25,-5
29,-8
7,7
7,3
9,-2
11,-3
13,-4
30,-8
28,-10
27,-9
30,-9
30,-5
29,-6
6,8
20,-10
8,-1
28,-8
15,-2
26,-7
7,6
7,0
10,-2
30,-7
21,-8
24,-7
22,-6
11,-2
6,7
21,-9
29,-9
12,-2
7,1
28,-6
9,-1
11,-1
28,-5
22,-7
21,-7
20,-5
6,4
6,2
15,-3
28,-9
23,-9
11,-4
10,-1
20,-9
21,-10
24,-9
9,0
29,-10
6,1
20,-7
22,-5
12,-3
6,0
12,-4
26,-5
14,-2
7,9
20,-6
27,-7
6,3
14,-4
30,-10
26,-8
24,-6
22,-10
26,-9
22,-9
29,-7
6,6
6,9
24,-5
28,-7
21,-6
14,-3
25,-8
23,-7
27,-6
7,4
6,5
13,-3
21,-5
29,-5"""


def part1(target: str):
    nums = utils.extractInts(target)
    x_range = range(nums[0], nums[1] + 1)
    y_range = range(nums[2], nums[3] + 1)

    # First find all the x velocities that get us in the target
    # and keep track of the time spots. Then we want the highest y that
    # hits the target in an appropriate timeslot
    valid_times: Set[int] = set()
    min_x0 = 9999
    for xv in range(1, x_range[-1]):
        positions = x_positions(xv)
        for xpos, time, vel in positions:
            if xpos in x_range:
                valid_times.add(time)
                print(f"xv={xv} xpos={xpos} time={time} vel={vel}")
                if vel == 0:
                    # can accept any time beyond this
                    min_x0 = min(time, min_x0)
                    print(f"Found an x0: {time} {min_x0}")
            if xpos > x_range[-1]:
                break
            if vel == 0:
                # Too short
                break

    print(f"Valid times are >{min_x0} and: {valid_times}")

    # Now find a yv that will get us there while remaining in x time slots (which appear to be anything)
    max_y = 0
    for yv in range(y_range[0], 1000):
        positions = y_positions(yv)
        vel_max_y = 0
        for ypos, time in positions:
            vel_max_y = max(vel_max_y, ypos)
            if ypos in y_range:
                # hit the target
                print(f"Hit the target with yv={yv} at time={time} vel_max_y={vel_max_y}")
                max_y = max(max_y, vel_max_y)
            if ypos < y_range[0]:
                # missed
                break

    print(f"Max Y encountered {max_y}")


def part2(target: str):
    nums = utils.extractInts(target)
    x_range = range(nums[0], nums[1] + 1)
    y_range = range(nums[2], nums[3] + 1)

    # First find all the x velocities that get us in the target
    # and keep track of the time spots. Then we want the highest y that
    # hits the target in an appropriate timeslot
    time_xs: Dict[int, Set[int]] = defaultdict(set)
    for xv in range(1, x_range[-1]+1):
        positions = x_positions(xv)
        for xpos, time, vel in positions:
            if xpos in x_range:
                time_xs[time].add(xv)
                print(f"xv={xv} xpos={xpos} time={time} vel={vel}")
                if vel == 0:
                    # can accept any time beyond this
                    for t in range(time, 500):
                        time_xs[t].add(xv)
            if vel == 0 or xpos > x_range[-1]:
                break

    time_ys: Dict[int, Set[int]] = defaultdict(set)
    for yv in range(y_range[0], 1000):
        positions = y_positions(yv)
        for ypos, time in positions:
            if ypos in y_range:
                # hit the target
                time_ys[time].add(yv)
            if ypos < y_range[0]:
                # missed
                break

    # Now calculate
    combos: Set[Tuple[int, int]] = set()
    for t in time_ys:
        print(f"Time: {t} Xs={time_xs[t]} Ys={time_ys[t]}")
        for xv in time_xs[t]:
            for xy in time_ys[t]:
                combos.add( (xv, xy))
    print(combos)
    print(len(combos))
    expected = get_expected()
    missing = expected.difference(combos)
    print(f"Missing {missing}")


def get_expected() -> Set[Tuple[int, int]]:
    splits = [utils.extractInts(s) for s in test_expected.splitlines()]
    tuples = {(e[0], e[1]) for e in splits}
    return tuples



def x_positions(velocity: int) -> Tuple[int, int, int]:
    time = 0
    x = 0
    v = velocity
    while True:
        time += 1
        x += v
        if v > 0:
            v -= 1
        yield x, time, v


def y_positions(velocity: int) -> Tuple[int, int]:
    time = 0
    y = 0
    v = velocity
    while True:
        time += 1
        y += v
        v -= 1
        yield y, time


if __name__ == "__main__":
    part2(test_input)
    part2(data)
    # part1(data)




