from __future__ import annotations

import unittest
from collections import Iterator, Iterable
from dataclasses import dataclass, field
from typing import List, Set, Tuple, Optional

import aocd

from aoc import utils

test_input2 = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""


@dataclass(frozen=True, order=True)
class Coord:
    x: int
    y: int
    z: int

    def min(self, other: Coord) -> Coord:
        return Coord(min(self.x, other.x), min(self.y, other.y), min(self.z, other.z))

    def max(self, other: Coord) -> Coord:
        return Coord(max(self.x, other.x), max(self.y, other.y), max(self.z, other.z))

    def mid(self, other: Coord) -> Coord:
        return Coord((self.x + other.x) // 2, (self.y + other.y) // 2, (self.z + other.z) // 2)


@dataclass(frozen=True, order=True)
class Cuboid:
    min_bound: Coord
    max_bound: Coord

    def bounds(self) -> Iterator[Coord]:
        yield self.min_bound
        yield self.max_bound

    def points(self) -> Iterator[Coord]:
        for x in range(self.min_bound.x, self.max_bound.x + 1):
            for y in range(self.min_bound.y, self.max_bound.y + 1):
                for z in range(self.min_bound.z, self.max_bound.z + 1):
                    coord = Coord(x, y, z)
                    # print(f"Yielding: {coord}")
                    yield coord

    def midpoint(self) -> Coord:
        return self.min_bound.mid(self.max_bound)

    def point_inside(self, p: Coord) -> bool:
        return (self.min_bound.x <= p.x <= self.max_bound.x and
                self.min_bound.y <= p.y <= self.max_bound.y and
                self.min_bound.z <= p.z <= self.max_bound.z)

    def count_inside(self, ps: Iterable[Coord]) -> int:
        return len([p for p in ps if self.point_inside(p)])

    def contains(self, c: Cuboid) -> bool:
        return self.count_inside(c.bounds()) == 2

    #
    # def overlaps(self, c: Cuboid) -> bool:
    #     return self.count_inside(c.bounds()) == 1

    def disjoint(self, c: Cuboid) -> bool:
        return self.intersection(c) is None

    def size(self):
        return (
                (self.max_bound.x - self.min_bound.x + 1) *
                (self.max_bound.y - self.min_bound.y + 1) *
                (self.max_bound.z - self.min_bound.z + 1)
        )

    def intersection(self, c: Cuboid) -> Optional[Cuboid]:
        int_min = self.min_bound.max(c.min_bound)
        int_max = self.max_bound.min(c.max_bound)
        # Check if the intersection actually intersects
        int_cuboid = Cuboid(int_min, int_max)
        if not self.point_inside(int_cuboid.midpoint()):
            return None
        return Cuboid(int_min, int_max)

    @classmethod
    def create(cls, line: str) -> Cuboid:
        # on x=10..12,y=10..12,z=10..12
        nums = utils.extractInts(line)
        min_b = Coord(min(nums[0], nums[1]), min(nums[2], nums[3]), min(nums[4], nums[5]))
        max_b = Coord(max(nums[0], nums[1]), max(nums[2], nums[3]), max(nums[4], nums[5]))
        return Cuboid(min_b, max_b)


@dataclass
class Region:
    on: bool
    c: Cuboid
    subtractions: List[Region] = field(default_factory=list)

    def switch_off(self, off: Cuboid) -> bool:
        """Returns true if it intersected"""
        # Determine if it intersects with me
        if self.c.disjoint(off):
            return False
        c_int = self.c.intersection(off)
        r = Region(False, c_int)
        # Now, compare this will all existing subtractions
        for s in self.subtractions:
            if s.switch_off(c_int):
                # Some part overlapped - remove that from the region
                sub_int = s.c.intersection(c_int)
                r.subtractions.append(Region(True, sub_int))
        # now if there's anything left of our region, we can add it to the subtractions
        if self.on and r.size() > 0:
            self.subtractions.append(r)
        return True

    def switch_on(self, on: Cuboid) -> bool:
        """Returns true if it intersected"""
        # Determine if it intersects with me
        if self.c.disjoint(on):
            return False
        c_int = self.c.intersection(on)
        r = Region(True, c_int)
        # Now, compare this will all existing subtractions
        for s in self.subtractions:
            if s.switch_on(c_int):
                # Some part overlapped - remove that from the region
                sub_int = s.c.intersection(c_int)
                r.subtractions.append(Region(False, sub_int))
        # now if there's anything left of our region, we can add it to the subtractions
        if not self.on and r.size() > 0:
            self.subtractions.append(r)
        return True

    def size(self):
        s = self.c.size()
        for r in self.subtractions:
            s -= r.size()
        return s


def part1(lines: List[str]) -> int:
    c = Cuboid.create("-50..50 -50..50 -50..50")
    lights: Set[Coord] = set()
    for line in lines:
        on = line.strip().startswith("on")
        c1 = Cuboid.create(line)
        if not c.disjoint(c1):
            # get the intersection
            c_int = c.intersection(c1)
            if on:
                lights.update(c_int.points())
            else:
                lights.difference_update(c_int.points())
        else:
            # Ignore it
            pass
    return len(lights)


def part2_analyse(lines: List[str]):
    inst: List[Tuple[bool, Cuboid]] = []
    for line in lines:
        on = line.strip().startswith("on")
        c1 = Cuboid.create(line)
        inst.append((on, c1))
    # Now see how many could be eliminated by being completely contained
    min_bound = Coord(0, 0, 0)
    max_bound = Coord(0, 0, 0)
    for i, c in enumerate(inst):
        intersection_found = False
        for j in range(i + 1, len(inst)):
            if inst[j][1].contains(c[1]):
                print(f"Cube {c} eliminated by {inst[j]}")
            if not inst[j][1].disjoint(c[1]):
                intersection_found = True
        if not intersection_found:
            print(f"Cube {c} is disjoint with all following it")
        min_bound = min_bound.min(c[1].min_bound)
        max_bound = max_bound.max(c[1].max_bound)

    print(f"Bounds {min_bound} to {max_bound}")


def part2(lines: List[str]) -> int:
    cuboids: List[Tuple[Cuboid, int]] = []
    for line in lines:
        on = line.strip().startswith("on")
        c1 = Cuboid.create(line)
        cuboids.append((c1, 1 if on else -1))
    # Now we have them all, apply
    result: List[Tuple[Cuboid, int]] = [cuboids[0]]
    for i, op in cuboids[1:]:
        for j, jop in result.copy():
            c = i.intersection(j)
            cop = 1
            if c:
                if jop == 1:
                    cop = -1
                result.append((c, cop))
        if op == 1:
            result.append((i, op))
    answer = 0
    for c, op in result:
        answer += c.size() * op
    print(f"Answer: {answer}")
    return answer


class Day22Test(unittest.TestCase):
    def test_inside(self):
        c = Cuboid.create("x=10..-10,y=10..-10,z=10..-10")
        self.assertTrue(c.point_inside(Coord(0, 0, 0)))
        self.assertTrue(c.point_inside(Coord(-1, -1, -1)))
        self.assertTrue(c.point_inside(Coord(-10, -10, -10)))
        self.assertFalse(c.point_inside(Coord(-10, -10, -11)))
        c1 = Cuboid.create("x=1..-1,y=1..-1,z=1..-1")
        self.assertFalse(c.disjoint(c1))
        c2 = Cuboid.create("x=9..-11,y=9..-11,z=10..-10")
        self.assertFalse(c.disjoint(c2))

    def test_size(self):
        self.assertEqual(27, Cuboid.create("on x=10..12,y=10..12,z=10..12").size())

    def test_points(self):
        c = Cuboid.create("on x=10..12,y=10..12,z=10..12")
        self.assertEqual(27, len(set(c.points())))
        self.assertEqual(27, len(set([p for p in c.points() if c.point_inside(p)])))

    def test_intersection(self):
        c1 = Cuboid.create("on x=0..10,y=0..10,z=0..10")
        self.assertEqual(c1, c1.intersection(c1))
        # Completely contained
        c2 = Cuboid.create("on x=2..4,y=2..4,z=2..4")
        self.assertEqual(c2, c1.intersection(c2))
        self.assertEqual(c2, c2.intersection(c1))
        # Overlap with 1 inside
        c3 = Cuboid.create("on x=2..14,y=2..14,z=2..14")
        self.assertEqual(Cuboid.create("x=2..10,y=2..10,z=2..10"), c1.intersection(c3))
        self.assertEqual(Cuboid.create("x=2..10,y=2..10,z=2..10"), c3.intersection(c1))
        # Overlap completely external
        c4 = Cuboid.create("x=2..4,y=2..4,z=-100..100")
        self.assertEqual(Cuboid.create("x=2..4,y=2..4,z=0..10"), c1.intersection(c4))
        self.assertEqual(Cuboid.create("x=2..4,y=2..4,z=0..10"), c4.intersection(c1))
        # Disjoint
        c5 = Cuboid.create("x=20..40,y=20..40,z=20..40")
        with self.assertRaises(ValueError):
            c1.intersection(c5)

    def test_part1_test(self):
        test_input = """on x=10..12,y=10..12,z=10..12
            on x=11..13,y=11..13,z=11..13
            off x=9..11,y=9..11,z=9..11
            on x=10..10,y=10..10,z=10..10"""
        self.assertEqual(39, part1(test_input.splitlines()))

        test_input1 = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""
        self.assertEqual(590784, part1(test_input1.splitlines()))

        self.assertEqual(474140, part1(test_input2.splitlines()))

    def test_part1(self):
        result = part1(aocd.data.splitlines())
        print(f"{result}")
        self.assertEqual(602574, result)

    def test_part2(self):
        part2_analyse(test_input2.splitlines())
        universe = Region(False, Cuboid(Coord(-150000, -150000, -150000), Coord(150000, 150000, 150000)))
        for line in test_input2.splitlines():
            on = line.strip().startswith("on")
            c1 = Cuboid.create(line)
            if on:
                universe.switch_on(c1)
            else:
                universe.switch_off(c1)
        print(f"Count: {universe.size()}")
        invert = sum([s.size() for s in universe.subtractions])
        print(f"Inverse: {invert}")
        print(f"{universe.size() - invert} {universe.size() + invert}")

    def test_part2a(self):
        self.assertEqual(2758514936282235, part2(test_input2.splitlines()))

    def test_part2_real(self):
        self.assertEqual(1288707160324706, part2(aocd.data.splitlines()))

    def test_switch_off(self):
        c = Cuboid.create("0..9, 0..9, 0..9")
        r = Region(True, c)
        to_remove = Cuboid.create("0..4, 0..4, 0..4")
        r.switch_off(to_remove)
        self.assertEqual(125, to_remove.size())
        self.assertEqual(1000, c.size())
        self.assertEqual(875, r.size())
        back_on = Cuboid.create("1..2, 1..2, 1..2")
        r.switch_on(back_on)
        self.assertEqual(883, r.size())
        # Switch off something that's already off
        to_remove2 = Cuboid.create("0..5, 0..5, 0..5")
        r.switch_off(to_remove2)
        self.assertEqual(784, r.size())
