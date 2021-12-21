from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

test_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


@dataclass
class Position:
    row: int
    col: int


class Board:
    def __init__(self, numbers: Dict[int, Position]):
        self.numbers: Dict[int, Position] = numbers
        self.rows = [0, 0, 0, 0, 0]
        self.cols = [0, 0, 0, 0, 0]

    def mark(self, value: int) -> bool:
        pos = self.numbers.get(value)
        if pos:
            self.rows[pos.row] += 1
            self.cols[pos.col] += 1
            # remove the number
            self.numbers.pop(value)
            # Return true if complete
            return self.rows[pos.row] == 5 or self.cols[pos.col] == 5
        return False

    def sum(self) -> int:
        return sum(self.numbers.keys())

    def __str__(self):
        return str(self.numbers)

    @classmethod
    def parse(cls, lines: List[str]) -> "Board":
        result: Dict[int, Position] = {}
        row = 0
        while lines:
            line = lines.pop(0).strip()
            if line:
                print(f"Parsing: {line}")
                vals = [int(v) for v in line.split()]
                for col in range(0, 5):
                    result[vals[col]] = Position(row, col)
                row += 1
            else:
                return Board(result)
        return Board(result)

if __name__ == "__main__":
    lines = [l.strip() for l in Path("day4.txt").read_text().splitlines()]
    # lines = test_input.splitlines()
    calls = [int(l) for l in lines.pop(0).split(",")]
    lines.pop(0)
    print(calls)
    boards: List[Board] = []

    while True:
        board = Board.parse(lines)
        if board:
            boards.append(board)
        if not lines:
            break


    print(len(boards))
    print(boards[0])
    print(boards[1])
    print(boards[2])
    # Now do all the calls until we have a line

    # 6230 too low

    finished = False
    for c in calls:
        if finished or len(boards) == 0:
            break
        completed = []
        for b in boards:
            if finished:
                break
            if b.mark(c):
                print(f"Board completed: {b}")
                print(f"Board sum: {b.sum()}")
                print(f"answer: {b.sum() * c}")
                completed.append(b)
                # finished = True
        # Now remove the completed boards
        for com in completed:
            boards.remove(com)
        print(f"Boards remaining: {len(boards)}")

