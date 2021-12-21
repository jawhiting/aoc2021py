import timeit
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Callable, Set, Dict, Optional, Tuple

from utils import extractInts, RowCol, Coord
from aocd import data
import heapq

test_input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


def part1(lines: List[str]):
    dijkstra(intify(lines), RowCol(0, 0), RowCol(len(lines) - 1, len(lines[0]) - 1))


def part2(lines: List[str]):
    grid = bigify(intify(lines))
    # for row in grid:
    #     print("".join([str(i) for i in row]))

    print(timeit.timeit(lambda: dijkstra(grid, RowCol(0, 0), RowCol(len(grid) - 1, len(grid[0]) - 1)), number=1))
    print(timeit.timeit(lambda: dijkstra2(grid, RowCol(0, 0), RowCol(len(grid) - 1, len(grid[0]) - 1)), number=1))


def intify(lines: List[str]) -> List[List[int]]:
    result = []
    for line in lines:
        result.append([int(c) for c in line])
    return result


def bigify(grid: List[List[int]], factor=5) -> List[List[int]]:
    new_grid = []
    for r in range(len(grid) * factor):
        source_r = r % len(grid)
        inc_r = r // len(grid)
        row: List[int] = []
        for c in range(len(grid[0]) * factor):
            source_c = c % len(grid[0])
            inc_c = c // len(grid[0])
            inc_cell = inc_r + inc_c
            next_val = (grid[source_r][source_c] + inc_cell - 1) % 9 + 1
            row.append(next_val)
        new_grid.append(row)
    return new_grid


def dijkstra(grid: List[List[int]], start: RowCol, target: RowCol) -> int:
    to_visit: List[Tuple[int, RowCol]] = []
    visited: Set[RowCol] = set()
    heapq.heappush(to_visit, (0, start))
    distance: Dict[RowCol, int] = {start: 0}
    print(f"Target: {target}")
    while to_visit:
        # Get the next cell to visit
        dist, cell = heapq.heappop(to_visit)

        # Now check each neighbour
        for n in cell.neighbours4():
            try:
                n_dist = dist + grid[n.row][n.col]
                if n not in distance or n_dist < distance[n]:
                    # New shortest path
                    distance[n] = n_dist
                if n not in visited:
                    heapq.heappush(to_visit, (n_dist, n))
                    visited.add(n)
            except IndexError:
                pass
        # print(f"Visited: {cell} {len(visited)} ToVisit: {len(to_visit)}")
    # Now we should be finished
    print(f"Distance {distance[target]}")
    return distance[target]


def cell_index(pos: RowCol) -> int:
    return pos.row * 500 + pos.col


def dijkstra2(grid: List[List[int]], start: RowCol, target: RowCol) -> int:
    to_visit: List[Tuple[int, RowCol]] = []
    heapq.heappush(to_visit, (0, start))
    visited: List[bool] = [False] * (500 * 500)
    distance: List[int] = [999999] * (500 * 500)
    distance[0] = 0
    visited[0] = True
    print(f"Target: {target}")
    while to_visit:
        # Get the next cell to visit
        dist, cell = heapq.heappop(to_visit)
        # Now check each neighbour
        for n in cell.neighbours4():
            try:
                n_dist = dist + grid[n.row][n.col]
                idx = n.row*500 + n.col
                if n_dist < distance[idx]:
                    # New shortest path
                    distance[idx] = n_dist
                if not visited[idx]:
                    heapq.heappush(to_visit, (n_dist, n))
                    visited[idx] = True
            except IndexError:
                pass
        # print(f"Visited: {cell} {len(visited)} ToVisit: {len(to_visit)}")
    # Now we should be finished
    print(f"Distance {distance[cell_index(target)]}")
    return distance[cell_index(target)]


if __name__ == "__main__":
    part1(test_input.splitlines())
    part1(data.splitlines())
    part2(test_input.splitlines())
    part2(data.splitlines())
