import itertools
import unittest
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterator, Iterable, Dict


def deterministic_die(r: range) -> Iterator[int]:
    while True:
        for v in r:
            yield v

@dataclass
class Game:
    start1: int
    start2: int
    pos1: int = 0
    pos2: int = 0
    score1: int = 0
    score2: int = 0
    die: Iterator[int] = deterministic_die(range(1, 101))
    turns = 0

    def reset(self):
        self.pos1 = self.start1
        self.pos2 = self.start2
        # reset die
        self.die = deterministic_die(range(1, 101))
        self.score1 = 0
        self.score2 = 0
        self.turns = 0


    def play(self, target=1000):
        self.reset()
        while True:
            if self.turn1(target):
                score_ = self.turns * 3 * self.score2
                print(f"Player 1 wins {self.turns} rolls={self.turns*3} losing={self.score2} Result={score_}")
                return score_
            if self.turn2(target):
                score_ = self.turns * 3 * self.score1
                print(f"Player 2 wins {self.turns} rolls={self.turns*3} losing={self.score1} Result={score_}")
                return score_

    def turn1(self, target: int) -> bool:
        p1move = sum(itertools.islice(self.die, 3))
        # Check if we're back to start of cycle
        if self.pos1 == self.start1 and self.pos2 == self.start2 and p1move == 6:
            print(f"Turn {self.turns} - back to start. P1={self.score1} P2={self.score2}")
        self.pos1 = ((self.pos1-1) + p1move)%10+1
        self.score1 += self.pos1
        self.turns += 1
        print(f"P1 Turn {self.turns} P1Pos={self.pos1} P2Pos={self.pos2} P1Score={self.score1} P2Score={self.score2}")
        return self.score1 >= target

    def turn2(self, target: int) -> bool:
        p2move = sum(itertools.islice(self.die, 3))
        self.pos2 = ((self.pos2-1) + p2move)%10+1
        self.score2 += self.pos2
        self.turns += 1
        print(f"P2 Turn {self.turns} P1Pos={self.pos1} P2Pos={self.pos2} P1Score={self.score1} P2Score={self.score2}")
        return self.score2 >= target

# Score 3: 111 -> 1 universe
# Score 4: 112 121 211 -> 3 universe
# score 5: 311 131 113 122 212 221 -> 6
# score 6: 123 132 213 312 231 321 222 -> 7
# score 7: 133 313 331 322 232 331 -> 6
# Score 8: 332 323 233 -> 3 universe
# Score 9: 333 -> 1 universe
quantum_die = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}


def next_pos(pos: int, move: int) -> int:
    return ((pos - 1) + move) % 10 + 1


@dataclass(frozen=True, order=True)
class UniverseKey:
    pos1: int
    pos2: int
    score1: int
    score2: int

@dataclass
class Game2:
    universes: Dict[UniverseKey, int] = field(default_factory=dict)

    def play(self, start1: int, start2: int, target=21) -> int:
        # Create the current universe
        self.universes[UniverseKey(start1, start2, 0, 0)] = 1
        # Now iterate until there are none left
        win1 = 0
        win2 = 0
        p1_next = True
        while self.universes:
            next_universes: Dict[UniverseKey, int] = {}
            for universe, count in self.universes.items():
                # move whichever player
                if p1_next:
                    # Player 1
                    for move, versions in quantum_die.items():
                        p = next_pos(universe.pos1, move)
                        s = universe.score1 + p
                        # if its a winner
                        if s >= 21:
                            win1 += count * versions
                        else:
                            next_key = UniverseKey(p, universe.pos2, s, universe.score2)
                            if next_key in next_universes:
                                # increment
                                next_universes[next_key] += count*versions
                            else:
                                next_universes[next_key] = count * versions
                else:
                    # Player 2
                    for move, versions in quantum_die.items():
                        p = next_pos(universe.pos2, move)
                        s = universe.score2 + p
                        if s == 0:
                            break
                        # if its a winner
                        if s >= 21:
                            win2 += count * versions
                        else:
                            next_key = UniverseKey(universe.pos1, p, universe.score1, s)
                            if next_key in next_universes:
                                # increment
                                next_universes[next_key] += count * versions
                            else:
                                next_universes[next_key] = count * versions
            self.universes = next_universes
            p1_next = False if p1_next else True
        print(f"Win1: {win1} Win2: {win2}")
        return max(win1, win2)



class Day21Test(unittest.TestCase):

    def test_die(self):
        d = deterministic_die(range(5))
        for i in range(11):
            print(next(d))

    def test_game(self):
        game = Game(4, 8)
        self.assertEqual(739785, game.play())

    def test_part1(self):
        game = Game(10, 4)
        self.assertEqual(908091, game.play())

    def test_part2_test(self):
        self.assertEqual(444356092776315, Game2().play(4, 8))

    def test_part2(self):
        self.assertEqual(190897246590017, Game2().play(10, 4))
