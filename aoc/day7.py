# from functools import cache
from typing import List, Callable

from utils import extractInts
from aocd import data

test_input = "16,1,2,0,4,2,7,1,2,14"
input = data


def part1(nums: List[int]) -> int:
    # pick an initial pos
    pos = sum(nums) // len(nums)
    minimise(0, nums, lambda t, n: distance(t, n, fuel_cost_1))
    minimise(len(nums), nums, lambda t, n: distance(t, n, fuel_cost_1))


def part2(nums: List[int]) -> int:
    # pick an initial pos
    pos = sum(nums) // len(nums)
    minimise(0, nums, lambda t, n: distance(t, n, fuel_cost_2))
    minimise(len(nums), nums, lambda t, n: distance(t, n, fuel_cost_2))


def minimise(pos: int, nums: List[int], cost_fn: Callable[[int, List[int]], int]) -> int:
    cost = cost_fn(pos, nums)
    # figure out direction
    left_cost = cost_fn(pos - 1, nums)
    right_cost = cost_fn(pos + 1, nums)
    inc = 1
    if left_cost < cost:
        inc = -1
    elif right_cost > cost:
        inc = 1
    else:
        print(f"Min: {pos} {cost}")

    next_cost = cost_fn(pos + inc, nums)
    iters = 0
    while next_cost < cost:
        iters += 1
        pos += inc
        cost = next_cost
        next_cost = cost_fn(pos + inc, nums)

    print(f"Position: {pos} Cost: {cost} Inc: {inc} NextCost: {next_cost} Iters: {iters}")


def distance(target: int, nums: List[int], cost_fn: Callable[[int, int], int]) -> int:
    return sum([cost_fn(target, d) for d in nums])


def fuel_cost_1(target: int, pos: int) -> int:
    return abs(target - pos)


def fuel_cost_2(target: int, pos: int) -> int:
    return sumseq(abs(target - pos))


def sumseq(n: int) -> int:
    return (n + 1) * n // 2


part1(extractInts(test_input))
part1(extractInts(input))
part2(extractInts(test_input))
part2(extractInts(input))
