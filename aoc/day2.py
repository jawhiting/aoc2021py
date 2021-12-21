from pathlib import Path
from typing import List


def part1(lines: List[str]):
    pos = [0,0]
    for l in lines:
        parts = l.split(" ")
        dir = parts[0]
        val = int(parts[1])
        if dir == "forward":
            pos[0] += val
        elif dir == "up":
            pos[1] -= val
        elif dir == "down":
            pos[1] += val

    print(pos[0] * pos[1])

# Part2
def part2(lines: List[str]):
    aim = 0
    pos = [0,0]

    for l in lines:
        parts = l.split(" ")
        dir = parts[0]
        val = int(parts[1])
        if dir == "forward":
            pos[0] += val
            pos[1] += val * aim
        elif dir == "up":
            aim -= val
        elif dir == "down":
            aim += val

    print(pos[0] * pos[1])

input = Path("day2.txt").read_text()
lines = [l.strip() for l in input.splitlines()]
part1(lines)
part2(lines)



