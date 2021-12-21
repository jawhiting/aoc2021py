from pathlib import Path
from typing import List

test_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

def part1(lines: List[str]):
    nums = [int(l, 2) for l in lines]
    num_count = len(nums)
    print(num_count)
    gamma = 0
    epsilon = 0
    for b in range(0, len(lines[0])):
        # For each byte position
        mask = 2**b
        set_count = sum([x & mask > 0 for x in nums])
        if set_count > num_count/2:
            print(f"Position {b} bit count {set_count} is 1")
            gamma += mask
        else:
            print(f"Position {b} bit count {set_count} is 0")
            epsilon += mask

    # too low: 369400
    # too low: 779000
    print(f"gamma: {gamma} epsilon: {epsilon} result: {gamma*epsilon}")

# Part2
def part2(lines: List[str]):
    nums = [int(l, 2) for l in lines]
    max_pos = len(lines[0])-1
    oxygen_nums = nums.copy()
    oxy = 0
    scrub = 0
    for i in range(0, len(lines[0])):
        pos = max_pos-i
        # Now only keep matches
        mask = 2**pos
        target = most_common_mask(pos, oxygen_nums)
        print(f"Most common is {mask}")
        oxygen_nums = [o for o in oxygen_nums if o & mask == target]
        if len(oxygen_nums) == 1:
            print(f"Filtered to 1: {oxygen_nums[0]}")
            oxy = oxygen_nums[0]
            break
        else:
            print(f"Reduced to {len(oxygen_nums)}")

    scrubber_nums = nums.copy()
    for i in range(0, len(lines[0])):
        pos = max_pos-i
        # Now only keep matches
        mask = 2**pos
        target = least_common_mask(pos, scrubber_nums)
        print(f"Least common is {target}")
        scrubber_nums = [s for s in scrubber_nums if s & mask == target]
        if len(scrubber_nums) == 1:
            print(f"Filtered to 1: {scrubber_nums[0]}")
            scrub = scrubber_nums[0]
            break
        else:
            print(f"Reduced to {len(scrubber_nums)}")

    print(f"Oxygen: {oxy} Scrubber: {scrub} Result: {oxy*scrub}")

def most_common_mask(pos: int, nums: List[int]) -> int:
    mask = 2**pos
    set_count = sum([x & mask > 0 for x in nums])
    return mask if set_count >= len(nums) / 2 else 0


def least_common_mask(pos: int, nums: List[int]) -> int:
    mask = 2**pos
    set_count = sum([x & mask > 0 for x in nums])
    print(f"LCM set count {set_count}")
    unset_count = len(nums) - set_count
    return 0 if unset_count <= len(nums) / 2 else mask


lines = [l.strip() for l in Path("day3.txt").read_text().splitlines()]
test_lines = test_input.splitlines()
part1(test_lines)
part1(lines)
part2(test_lines)
part2(lines)
