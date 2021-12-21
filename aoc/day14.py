from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Callable, Set, Dict, Optional, Tuple

from utils import extractInts, RowCol, Coord
from aocd import data

test_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

rules: Dict[str, str] = {}


def part1(lines: List[str]):
    target = lines.pop(0)
    rules.clear()
    cache.clear()
    for line in lines:
        if line:
            s = line.split(" -> ")
            rules[s[0].strip()] = s[1].strip()

    # Now apply x times
    result = expand_target(target, 10)
    minval = min(result.values())
    maxval = max(result.values())
    print(f"10 Min: {minval} Max: {maxval} Diff: {maxval - minval}")

    # cache.clear()
    result = expand_target(target, 40)
    minval = min(result.values())
    maxval = max(result.values())
    print(f"40 Min: {minval} Max: {maxval} Diff: {maxval-minval}")

    # Too high
    # 11231382237075658545002834024418459250988047799731689277457240086694367081515741830402559000974515244647399155511994

    # for d in range(1, 5):
    #     print(f"Running with depth {d}")
    #     c, s = expand("NN", d, rules)
    #     print(f"Depth: {d} Result: N{s}N")
    #     print(f"Counts: {c}")
    #     print(f"Countlen: {sum(c.values())} Explen: {len(s)}")


def expand_target(template: str, depth: int) -> Dict[str, int]:
    # Expand each pair in the template
    result = defaultdict(int)
    for c in template:
        result[c] += 1

    for i in range(len(template) - 1):
        added = get_expand(template[i] + template[i + 1], depth)
        for p, c in added.items():
            result[p] += c

    print(f"Result: {result}")
    print(f"Len: {sum(result.values())}")
    return result


cache: Dict[Tuple[str, int], Dict[str, int]] = {}


def memo(pair: str, depth: int, result: Dict[str, int]):
    cache[(pair, depth)] = result


def get_expand(pair: str, depth: int) -> Dict[str, int]:
    cache_key = (pair, depth)
    if cache_key in cache:
        return cache[cache_key]
    else:
        result = expand(pair, depth)
        cache[cache_key] = result
        return result


def expand(pair: str, depth: int) -> Dict[str, int]:
    # Return count of all the new elements added by this rule
    next_element = rules[pair]
    if depth == 1:
        return {next_element: 1}.copy()
    else:
        # Expand and recurse
        e1 = get_expand(pair[0] + next_element, depth - 1)
        e2 = get_expand(next_element + pair[1], depth - 1)
        result = defaultdict(int)
        for p, c in e1.items():
            result[p] += c
        for p, c in e2.items():
            result[p] += c
        # add next_element as well
        result[next_element] += 1
        return result


if __name__ == "__main__":
    part1(test_input.splitlines())
    part1(data.splitlines())
