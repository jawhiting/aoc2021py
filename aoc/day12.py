from __future__ import annotations

import timeit
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from typing import List, Callable, Set, Dict, Optional

from utils import extractInts, RowCol
from aocd import data

test_input1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

test_input2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

test_input3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


@dataclass()
class Cave:
    name: str
    small: bool
    exits: Set[Cave] = field(default_factory=set)
    visited: int = 0

    def __hash__(self):
        return hash(self.name)


Path = List[str]


def part1(lines: List[str]):
    caves = build_graph(lines)
    # Now we have a graph of the caves
    paths = navigate(caves["start"], caves["end"], ["start"], visited_small={"start"})
    print(f"There are {len(paths)}")
    # for p in paths:
    #     print(f"Path: {p}")


def navigate(current: Cave, target: Cave, path: List[str], visited_small: Set[str]) -> List[List[str]]:
    if current is target:
        return [path]
    # if i am small, add to visited
    if current.small:
        visited_small.add(current.name)
    # Now visit all valid exits
    paths: List[List[str]] = []
    for e in current.exits:
        if e.name not in visited_small:
            child_paths = navigate(e, target, copy(path) + [e.name], copy(visited_small))
            if child_paths:
                paths += child_paths

    return paths


def part2_opt(lines: List[str]):
    caves = build_graph(lines)
    caves["start"].visited = 2
    # Now we have a graph of the caves
    paths = navigate2_opt(caves["start"], caves["end"], False)
    print(f"Part 2 There are {paths}")


def navigate2_opt(current: Cave, target: Cave, double_visited: bool) -> int:
    if current is target:
        return 1
    my_double_visited = double_visited
    if current.small:
        current.visited += 1
        if current.visited == 2:
            my_double_visited = True
    # Now visit all valid exits
    paths = 0
    visit_limit = 1 if my_double_visited else 2
    for e in current.exits:
        # if we've already done our double visit
        if e.visited < visit_limit:
            paths += navigate2_opt(e, target, my_double_visited)

    # Decrement self-visit as we return up the stack
    if current.small:
        current.visited -= 1
    return paths


def build_graph(lines: List[str]) -> Dict[str, Cave]:
    caves: Dict[str, Cave] = dict()
    for line in lines:
        p = line.split("-")
        name = p[0].strip()
        to = p[1].strip()
        if to not in caves:
            caves[to] = Cave(to, to.islower())
        if name not in caves:
            caves[name] = Cave(name, name.islower())
        if to != "start" and name != "end":
            caves[name].exits.add(caves[to])
        if name != "start" and to != "end":
            caves[to].exits.add(caves[name])
    return caves


if __name__ == "__main__":
    # part1(test_input1.splitlines())
    # part1(test_input2.splitlines())
    # part1(test_input3.splitlines())
    # part1(data.splitlines())
    # part2(test_input1.splitlines())
    # part2(test_input2.splitlines())
    # part2(test_input3.splitlines())
    data_lines = data.splitlines()

    print(timeit.timeit(lambda: build_graph(data_lines), number=10))
    print(timeit.timeit(lambda: part2_opt(data_lines), number=10))
