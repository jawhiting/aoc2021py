from pathlib import Path
import aocd
input = Path("day1.txt").read_text()
lines = [int(l) for l in input.splitlines()]

increaseCount = 0
for i in range(1, len(lines)):
    if lines[i-1] < lines[i]:
        increaseCount += 1

print(f"Part1: {increaseCount}")

increaseCount = 0
for i in range(3, len(lines)):
    if lines[i] > lines[i-3]:
        increaseCount += 1

print(f"Part 2a: {increaseCount}")

print(aocd.data)