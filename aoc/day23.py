from __future__ import annotations

import heapq
import unittest
from dataclasses import dataclass
from typing import List, Iterable, Tuple, ClassVar, Set


distances = [
    [3, 5, 7, 9],
    [2, 4, 6, 8],
    [],
    [2, 2, 4, 6],
    [],
    [4, 2, 2, 4],
    [],
    [6, 4, 2, 2],
    [],
    [8, 6, 4, 2],
    [9, 7, 5, 3]
]

factors = {"A": 1, "B": 10, "C": 100, "D": 1000}


@dataclass(frozen=True, order=True)
class Burrow:
    positions: List[str]
    depth: int
    room_len: int
    c_start: ClassVar[int] = 0
    c_end: ClassVar[int] = 10
    room_entrances: ClassVar[List[int]] = [2, 4, 6, 8]
    room_indices: ClassVar[List[int]] = [15, 20, 25, 30]
    room_accepts: ClassVar[List[int]] = ["A", "B", "C", "D"]

    def moves(self) -> Iterable[Tuple[int, Burrow]]:
        # Calculate all possible moves and their cost from this
        # First, any in corridor try to move into every possible room
        for c in range(self.c_start, self.c_end + 1):
            if len(distances[c]) == 0:
                # skip the entrance spaces
                continue
            if self.positions[c] != ".":
                # Which rooms could we move to, and can we get there
                for r in self.available_rooms(self.positions[c]):
                    if self.can_get_to_room(c, r):
                        # make the move and yield
                        yield self.move_to_room(c, r)

        # Then, any in a room which haven't already moved try to move into any corridor spot
        for r in range(len(self.room_indices)):
            if self.room_locked(r):
                continue
            # Try all corridor spots that we can get to
            for c in self.accessible_from(r):
                yield self.move_to_corridor(r, c)

    def room_empty(self, r: int) -> bool:
        ri = self.room_indices[r]
        for i in range(self.room_len):
            if self.positions[ri + i] != ".":
                return False
        return True

    def room_locked(self, r: int) -> bool:
        return self.room_empty(r) or self.room_complete(r) or self.room_semi_complete(r)

    def room_complete(self, r: int) -> bool:
        ri = self.room_indices[r]
        room_type = self.room_accepts[r]
        for i in range(self.room_len):
            if self.positions[ri + i] != room_type:
                return False
        return True

    def room_semi_complete(self, r: int) -> bool:
        ri = self.room_indices[r]
        room_type = self.room_accepts[r]
        for i in range(self.room_len):
            if self.positions[ri + i] not in [room_type, "."]:
                return False
        return True

    def room_first(self, r: int) -> str:
        ri = self.room_indices[r]
        for i in range(self.room_len):
            if (a := self.positions[ri + i]) != ".":
                return a
        raise ValueError("Asked for first from empty room")

    def first_in(self, r: int) -> int:
        ri = self.room_indices[r]
        for i in range(self.room_len):
            if self.positions[ri + i] != '.':
                return i
        raise ValueError(f"No items in room {r}")

    def last_empty(self, r: int) -> int:
        ri = self.room_indices[r]
        for i in range(self.room_len):
            if self.positions[ri + i] != '.':
                if i < 1:
                    raise ValueError(f"Room already full: {r}")
                return i - 1
        # completely empty
        return self.room_len - 1

    def move_to_room(self, c: int, r: int) -> Tuple[int, Burrow]:
        """Return cost and new state"""
        dist_to_room = distances[c][r]
        dist_in_room = self.last_empty(r)
        a = self.positions[c]
        new_positions = self.positions.copy()
        new_positions[c] = "."
        new_positions[self.room_indices[r] + dist_in_room] = a
        return factors[a] * (dist_to_room + dist_in_room), Burrow(new_positions, self.depth + 1, self.room_len)

    def move_to_corridor(self, r: int, c: int) -> Tuple[int, Burrow]:
        dist_to_corridor = distances[c][r]
        dist_in_room = self.first_in(r)
        ri = self.room_indices[r]
        a = self.positions[ri + dist_in_room]
        if a == ".":
            raise ValueError("Invalid a")
        new_positions = self.positions.copy()
        new_positions[ri + dist_in_room] = "."
        new_positions[c] = a
        return factors[a] * (dist_in_room + dist_to_corridor), Burrow(new_positions, self.depth + 1, self.room_len)

    def available_rooms(self, a: str) -> Iterable[int]:
        # return index of viable rooms
        for room in range(len(self.room_indices)):
            # only if it matches the character
            if a != self.room_accepts[room]:
                continue
            # can move in if the room is empty
            if self.room_semi_complete(room):
                yield room

    def can_get_to_room(self, c: int, r: int) -> bool:
        dest = self.room_entrances[r]
        for i in range(c, dest, 1 if dest > c else -1):
            if i == c:
                continue
            if self.positions[i] != ".":
                return False
        return True

    def accessible_from(self, r: int) -> Iterable[int]:
        start = self.room_entrances[r]
        # left
        for c in range(start, self.c_start - 1, -1):
            # skip the special corridor spaces
            if len(distances[c]) == 0:
                continue
            if self.positions[c] == ".":
                yield c
            else:
                break
        # right
        for c in range(start, self.c_end + 1):
            # skip the special corridor spaces
            if len(distances[c]) == 0:
                continue
            if self.positions[c] == ".":
                yield c
            else:
                break

    @classmethod
    def create(cls, rooms: List[str], corridor="...........") -> Burrow:
        new_positions = ["."] * 35
        for r, rc in enumerate(rooms):
            ri = cls.room_indices[r]
            for i, a in enumerate(rc):
                new_positions[ri + i] = a
        for c, cc in enumerate(corridor):
            new_positions[c] = cc
        return Burrow(new_positions, 0, len(rooms[0]))

    def print(self) -> None:
        print(f"Depth: {self.depth}")
        print("#" + "".join(self.positions[self.c_start:self.c_end + 1]) + "#")
        for i in range(self.room_len):
            line = "###" if i == 0 else "  #"
            for r in self.room_indices:
                line += self.positions[r + i]
                line += "#"
            line += "##" if i == 0 else ""
            print(line)
        print("  #########  ")

    def complete(self) -> bool:
        # we are finished if all rooms contain the same letters
        for r in range(len(self.room_indices)):
            if not self.room_complete(r):
                return False
        return True

    def key(self) -> str:
        return "".join(self.positions)


def part1(b: Burrow, max_depth=35) -> int:
    seen_positions: Set[str] = set()
    heap: List[Tuple[int, Burrow]] = []
    heapq.heappush(heap, (0, b))
    cycle = 0
    while heap:
        cost, burrow = heapq.heappop(heap)
        if cycle % 1000 == 0:
            print(f"Heap is {len(heap)} depth={burrow.depth}")
        cycle += 1
        position_key = "".join(burrow.positions)
        if position_key in seen_positions:
            # print("Skipping already seen position")
            continue
        if burrow.complete():
            print(f"Found a completion: {cost}")
            burrow.print()
            return cost
        for c2, b2 in burrow.moves():
            if b2.depth <= max_depth:
                # don't add already seen
                if b2.key() in seen_positions:
                    continue
                heapq.heappush(heap, (cost + c2, b2))

        seen_positions.add(position_key)


class TestBurrow(unittest.TestCase):
    def test_create(self):
        b = Burrow.create(["BA", "CD", "BC", "DA"])
        self.assertEqual("B", b.positions[15])
        self.assertEqual("A", b.positions[16])
        self.assertEqual("C", b.positions[20])
        self.assertEqual("D", b.positions[21])
        self.assertEqual("B", b.positions[25])
        self.assertEqual("C", b.positions[26])
        self.assertEqual("D", b.positions[30])
        self.assertEqual("A", b.positions[31])
        b.print()

    def test_moves(self):
        b = Burrow.create(["BA", "CD", "BC", "DA"])
        i = 0
        for b1 in b.moves():
            print(f"Move {i} Cost: {b1[0]}")
            b1[1].print()
            i += 1

    def test_move_to_room(self):
        b = Burrow.create([".A", "CD", "BC", "DA"], "a..........")
        b.print()
        i = 0
        for b1 in b.moves():
            print(f"Move {i} Cost: {b1[0]}")
            b1[1].print()
            i += 1

    def test_available_rooms(self):
        b = Burrow.create([".A", "CD", "BC", "DA"], "a..........")
        self.assertEqual([0], list(b.available_rooms("a")))
        b2 = Burrow.create([".A", "..", "BC", "DA"], "a..........")
        self.assertEqual([0, 1], list(b2.available_rooms("a")))
        b3 = Burrow.create(["AA", "..", "BC", "DA"], "a..........")
        self.assertEqual([1], list(b3.available_rooms("a")))
        b4 = Burrow.create(["AA", "BB", "BC", "DA"], "a..........")
        self.assertEqual([], list(b4.available_rooms("a")))

    def test_can_get_to(self):
        b = Burrow.create(["..", "CD", "BC", "DA"], "b..a.......")
        self.assertTrue(b.can_get_to_room(0, 0))
        self.assertFalse(b.can_get_to_room(0, 1))
        self.assertFalse(b.can_get_to_room(0, 2))
        self.assertFalse(b.can_get_to_room(0, 3))

        b1 = Burrow.create(["..", "CD", "BC", "DA"], "...b.a.....")
        self.assertTrue(b1.can_get_to_room(3, 0))
        self.assertTrue(b1.can_get_to_room(3, 1))
        self.assertFalse(b1.can_get_to_room(3, 2))
        self.assertFalse(b1.can_get_to_room(3, 3))
        self.assertFalse(b1.can_get_to_room(5, 0))
        self.assertTrue(b1.can_get_to_room(5, 1))
        self.assertTrue(b1.can_get_to_room(5, 2))
        self.assertTrue(b1.can_get_to_room(5, 3))

    def test_room_complete(self):
        b = Burrow.create([".A", "AA", "aa", ".."], ".....d.d.a.")
        self.assertFalse(b.room_complete(0))
        self.assertTrue(b.room_complete(1))
        self.assertTrue(b.room_complete(2))
        self.assertFalse(b.room_complete(3))
        b1 = Burrow.create([".A", "AB", "aa", ".."], ".....d.d.a.")
        self.assertFalse(b1.room_complete(1))

    def test_cost(self):
        b = Burrow.create([".A", "BB", "CC", ".."], ".....D.D.A.")
        self.assertEqual(7008, part1(b))
        b1 = Burrow.create([".A", "BB", "CC", "DA"], ".....D.....")
        self.assertEqual(9011, part1(b1))
        b2 = Burrow.create(["BA", ".B", "CC", "DA"], ".....D.....")
        self.assertEqual(9051, part1(b2))
        b3 = Burrow.create(["BA", ".D", "CC", "DA"], "...B.......")
        self.assertEqual(12081, part1(b3))
        b4 = Burrow.create(["BA", "CD", ".C", "DA"], "...B.......")
        self.assertEqual(12481, part1(b4))

    def test_cost2(self):
        # b = Burrow.create(["BA", "CD", ".C", "DA"], "...B.......")
        # for m in b.moves():
        #     print(f"Cost {m[0]}")
        #     m[1].print()
        b = Burrow.create(["BA", ".D", ".C", "DA"], "...B.C.....")
        self.moves(b)

    @staticmethod
    def moves(b: Burrow):
        for m in b.moves():
            print(f"Cost {m[0]}")
            m[1].print()

    def test_part1(self):
        b = Burrow.create(["BA", "CD", "BC", "DA"])
        self.assertEqual(12521, part1(b))

    def test_part2(self):
        b = Burrow.create(["BDDA", "CCBD", "BBAC", "DACA"])
        self.assertEqual(44169, part1(b))

    def test_part2_real(self):
        b = Burrow.create(["BDDC", "BCBA", "DBAA", "DACC"])
        self.assertEqual(59071, part1(b))

    def test_part1_real(self):
        b = Burrow.create(["BC", "BA", "DA", "DC"])
        self.assertEqual(10607, part1(b))

    def test_complete(self):
        self.assertTrue(Burrow.create(["aA", "bB", "cC", "dD"]).complete())

    def test_part1_simple(self):
        b = Burrow.create([".A", "bB", "cC", "dD"], "a..........")
        i = 0
        for b1 in b.moves():
            print(f"Move {i} Cost: {b1[0]}")
            b1[1].print()
            i += 1

        part1(b)
