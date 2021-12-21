from dataclasses import dataclass
from typing import List, Type
import re

INT_PATTERN = re.compile("(-?[0-9]+)")


def extractInts(s: str) -> List[int]:
    return [int(n) for n in re.findall(INT_PATTERN, s)]


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass(frozen=True, order=True)
class RowCol:
    row: int
    col: int

    def neighbours4(self):
        for r in [self.row - 1, self.row + 1]:
            if r < 0:
                continue
            yield RowCol(r, self.col)
        for c in [self.col - 1, self.col + 1]:
            if c < 0:
                continue
            yield RowCol(self.row, c)

    def neighbours8(self):
        for r in [self.row - 1, self.row, self.row + 1]:
            if r < 0:
                continue
            for c in [self.col - 1, self.col, self.col + 1]:
                if c < 0 or (r == self.row and c == self.col):
                    continue
                yield RowCol(r, c)


@dataclass(unsafe_hash=True)
class Cell:
    val: int
    pos: RowCol


if __name__ == "__main__":
    t: Type = Cell
    print(str(t))
