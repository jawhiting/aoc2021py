from __future__ import annotations

import math
import unittest
from dataclasses import dataclass
from functools import cached_property
from itertools import permutations, combinations
from typing import List, Optional, Set, Iterator, Tuple

from aocd import data

from aoc import utils

test_input1 = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

part1_output = """Process finished with exit code 0
My: Coord(x=342, y=541, z=680) Their: Coord(x=447, y=-598, z=705)
Other scanner: Coord(x=-105, y=1139, z=-25)
Matched scan 0 with 4
My: Coord(x=587, y=-467, z=-517) Their: Coord(x=-442, y=-564, z=-571)
Other scanner: Coord(x=1029, y=97, z=54)
Matched scan 0 with 9
My: Coord(x=587, y=-467, z=-517) Their: Coord(x=639, y=610, z=-574)
Other scanner: Coord(x=-52, y=-1077, z=57)
Matched scan 0 with 15
My: Coord(x=587, y=-467, z=-517) Their: Coord(x=660, y=-500, z=545)
Other scanner: Coord(x=-73, y=33, z=-1062)
Matched scan 0 with 18
My: Coord(x=-579, y=596, z=796) Their: Coord(x=786, y=568, z=771)
Other scanner: Coord(x=-1365, y=28, z=25)
Matched scan 0 with 21
My: Coord(x=342, y=541, z=680) Their: Coord(x=449, y=483, z=-499)
Other scanner: Coord(x=-107, y=58, z=1179)
Matched scan 0 with 23
My: Coord(x=587, y=-467, z=-517) Their: Coord(x=-537, y=-546, z=707)
Other scanner: Coord(x=1124, y=79, z=-1224)
Matched scan 9 with 12
My: Coord(x=587, y=-467, z=-517) Their: Coord(x=640, y=656, z=646)
Other scanner: Coord(x=-53, y=-1123, z=-1163)
Matched scan 15 with 7
My: Coord(x=348, y=-491, z=716) Their: Coord(x=409, y=732, z=-545)
Other scanner: Coord(x=-61, y=-1223, z=1261)
Matched scan 15 with 28
My: Coord(x=-780, y=-1572, z=891) Their: Coord(x=-619, y=732, z=902)
Other scanner: Coord(x=-161, y=-2304, z=-11)
Matched scan 15 with 31
My: Coord(x=-597, y=711, z=-1920) Their: Coord(x=705, y=621, z=-855)
Other scanner: Coord(x=-1302, y=90, z=-1065)
Matched scan 18 with 33
My: Coord(x=-2051, y=851, z=472) Their: Coord(x=-818, y=739, z=-713)
Other scanner: Coord(x=-1233, y=112, z=1185)
Matched scan 21 with 24
My: Coord(x=1999, y=-719, z=-395) Their: Coord(x=-223, y=-697, z=694)
Other scanner: Coord(x=2222, y=-22, z=-1089)
Matched scan 12 with 16
My: Coord(x=1761, y=-803, z=-1871) Their: Coord(x=720, y=-775, z=440)
Other scanner: Coord(x=1041, y=-28, z=-2311)
Matched scan 12 with 29
My: Coord(x=-667, y=-387, z=-1845) Their: Coord(x=685, y=683, z=-640)
Other scanner: Coord(x=-1352, y=-1070, z=-1205)
Matched scan 7 with 30
My: Coord(x=-667, y=-387, z=-1845) Their: Coord(x=-631, y=749, z=470)
Other scanner: Coord(x=-36, y=-1136, z=-2315)
Matched scan 7 with 35
My: Coord(x=-958, y=-2860, z=828) Their: Coord(x=-867, y=744, z=678)
Other scanner: Coord(x=-91, y=-3604, z=150)
Matched scan 31 with 27
My: Coord(x=-2088, y=-760, z=-1780) Their: Coord(x=404, y=-702, z=-689)
Other scanner: Coord(x=-2492, y=-58, z=-1091)
Matched scan 33 with 1
My: Coord(x=-597, y=711, z=-1920) Their: Coord(x=645, y=-453, z=-825)
Other scanner: Coord(x=-1242, y=1164, z=-1095)
Matched scan 33 with 14
My: Coord(x=-2088, y=-760, z=-1780) Their: Coord(x=-717, y=-809, z=611)
Other scanner: Coord(x=-1371, y=49, z=-2391)
Matched scan 33 with 37
My: Coord(x=3143, y=-613, z=-1721) Their: Coord(x=754, y=-701, z=639)
Other scanner: Coord(x=2389, y=88, z=-2360)
Matched scan 16 with 8
My: Coord(x=2659, y=689, z=-291) Their: Coord(x=355, y=-494, z=842)
Other scanner: Coord(x=2304, y=1183, z=-1133)
Matched scan 16 with 32
My: Coord(x=355, y=-303, z=-3147) Their: Coord(x=-660, y=842, z=-766)
Other scanner: Coord(x=1015, y=-1145, z=-2381)
Matched scan 29 with 19
My: Coord(x=-2088, y=-760, z=-1780) Their: Coord(x=-770, y=354, z=591)
Other scanner: Coord(x=-1318, y=-1114, z=-2371)
Matched scan 30 with 26
My: Coord(x=-2088, y=-760, z=-1780) Their: Coord(x=305, y=-841, z=630)
Other scanner: Coord(x=-2393, y=81, z=-2410)
Matched scan 1 with 2
My: Coord(x=-3000, y=432, z=-1609) Their: Coord(x=-604, y=-878, z=-554)
Other scanner: Coord(x=-2396, y=1310, z=-1055)
Matched scan 1 with 10
My: Coord(x=-1654, y=-464, z=-2642) Their: Coord(x=-411, y=-572, z=945)
Other scanner: Coord(x=-1243, y=108, z=-3587)
Matched scan 37 with 34
My: Coord(x=3111, y=1855, z=-1907) Their: Coord(x=824, y=-628, z=-682)
Other scanner: Coord(x=2287, y=2483, z=-1225)
Matched scan 32 with 5
My: Coord(x=-854, y=-1670, z=-2974) Their: Coord(x=368, y=785, z=-552)
Other scanner: Coord(x=-1222, y=-2455, z=-2422)
Matched scan 26 with 36
My: Coord(x=-3000, y=432, z=-1609) Their: Coord(x=-460, y=-829, z=661)
Other scanner: Coord(x=-2540, y=1261, z=-2270)
Matched scan 2 with 13
My: Coord(x=-1654, y=-464, z=-2642) Their: Coord(x=827, y=-583, z=978)
Other scanner: Coord(x=-2481, y=119, z=-3620)
Matched scan 2 with 39
My: Coord(x=-3127, y=1811, z=-482) Their: Coord(x=-571, y=534, z=-595)
Other scanner: Coord(x=-2556, y=1277, z=113)
Matched scan 10 with 22
My: Coord(x=-1845, y=-720, z=-4286) Their: Coord(x=-565, y=-677, z=496)
Other scanner: Coord(x=-1280, y=-43, z=-4782)
Matched scan 34 with 3
My: Coord(x=-1693, y=-2799, z=-1864) Their: Coord(x=804, y=-506, z=397)
Other scanner: Coord(x=-2497, y=-2293, z=-2261)
Matched scan 36 with 25
My: Coord(x=-2133, y=1606, z=-2705) Their: Coord(x=345, y=-846, z=-358)
Other scanner: Coord(x=-2478, y=2452, z=-2347)
Matched scan 13 with 6
My: Coord(x=-3052, y=779, z=-4398) Their: Coord(x=712, y=710, z=-852)
Other scanner: Coord(x=-3764, y=69, z=-3546)
Matched scan 39 with 38
My: Coord(x=-2819, y=-1676, z=-2923) Their: Coord(x=-398, y=734, z=538)
Other scanner: Coord(x=-2421, y=-2410, z=-3461)
Matched scan 25 with 17
My: Coord(x=-4346, y=688, z=-3205) Their: Coord(x=523, y=570, z=294)
Other scanner: Coord(x=-4869, y=118, z=-3499)
Matched scan 38 with 11
My: Coord(x=-2988, y=-337, z=-4240) Their: Coord(x=681, y=832, z=-741)
Other scanner: Coord(x=-3669, y=-1169, z=-3499)
Matched scan 38 with 20
Base: 465
"""

part1_test_output = """Process finished with exit code 0
My: Coord(x=390, y=-675, z=-793) Their: Coord(x=322, y=571, z=-750)
Other scanner: Coord(x=68, y=-1246, z=-43)
Matched scan 0 with 1
My: Coord(x=-739, y=-1745, z=668) Their: Coord(x=-647, y=635, z=688)
Other scanner: Coord(x=-92, y=-2380, z=-20)
Matched scan 1 with 3
My: Coord(x=-345, y=-311, z=381) Their: Coord(x=-325, y=822, z=-680)
Other scanner: Coord(x=-20, y=-1133, z=1061)
Matched scan 1 with 4

My: Coord(x=408, y=-1815, z=803) Their: Coord(x=-697, y=-610, z=-426)

Ran 1 test in 3.556s
Other scanner: Coord(x=1105, y=-1205, z=1229)

OK
Matched scan 4 with 2
Base: 79"""


@dataclass(frozen=True)
class Coord:
    x: int
    y: int
    z: int

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def zrot(self):
        # 90 deg steps
        # cos 90 = 0, sin 90 = 1
        # x' = x*cos q - y*sin q
        # y' = x*sin q + y*cos q
        # z' = z
        # Therefore by 90 deg:
        # x' = -y
        # y' = x
        # z' = z
        return Coord(-self.y, self.x, self.z)
        pass

    def xrot(self):
        # y' = y*cos q - z*sin q
        # z' = y*sin q + z*cos q
        # x' = x
        return Coord(self.x, -self.z, self.y)
        pass

    def yrot(self):
        # z' = z*cos q - x*sin q
        # x' = z*sin q + x*cos q
        # y' = y
        return Coord(self.z, self.y, -self.x)

    def distance(self, other: Coord):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


@dataclass(frozen=True)
class Scan:
    id: int
    beacons: Set[Coord]

    def rebase(self, base: Coord):
        return Scan(self.id, {b - base for b in self.beacons})

    @cached_property
    def all_orientations(self) -> Set[Set[Coord]]:
        return set(self.orientations())

    def orientations(self) -> Iterator[Set[Coord]]:
        # calc all the orientations
        xo = self.beacons
        for x in range(4):
            xo = {c.xrot() for c in xo}
            yo = xo
            for y in range(4):
                yo = {c.yrot() for c in yo}
                zo = yo
                for z in range(4):
                    zo = frozenset({c.zrot() for c in zo})
                    yield zo

    def join(self, other: Scan):
        return Scan(self.id, self.beacons.union(other.beacons))

    @classmethod
    def parse(cls, lines: List[str]) -> Iterator[Scan]:
        scan_id = 0
        coords: Set[Coord] = set()
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("---"):
                    if coords:
                        yield Scan(scan_id, coords)
                    scan_id = utils.extractInts(line)[0]
                    coords = set()
                else:
                    nums = utils.extractInts(line)
                    coords.add(Coord(nums[0], nums[1], nums[2]))
        yield Scan(scan_id, coords)

    def intersect(self, other: Scan) -> Optional[Scan]:
        # for each of my coords
        mb = 0
        for my_base in self.beacons:
            my_rebased = {c - my_base for c in self.beacons}
            # For each of their orientations:
            mb += 1
            tor = 0
            for o in other.all_orientations:
                # for each of their coords
                tor += 1
                tc = 0
                for their_base in o:
                    tc += 1
                    their_rebased = {c - their_base for c in o}
                    # Now count the intersection
                    matches = my_rebased.intersection(their_rebased)
                    # print(f"{mb} {tor} {tc} Found {len(matches)}")
                    if len(matches) > 11:
                        # print(f"My: {my_base} Their: {their_base}")
                        # for m in matches:
                        #     print(f"{m + my_base}")
                        print(f"Other scanner: {my_base - their_base}")
                        return Scan(other.id, {c + my_base for c in their_rebased})


def join_scans(scans: List[Scan]) -> Scan:
    # take the first as the base
    base = scans[0]
    to_match: List[Scan] = [base]
    matched_scan_ids: Set[int] = {0}
    tested: Set[Tuple[int, int]] = set()
    while to_match:
        match_with = to_match.pop(0)
        for s in scans:
            key = (min(match_with.id, s.id), max(match_with.id, s.id))
            if s.id not in matched_scan_ids and key not in tested:
                result = match_with.intersect(s)
                if result:
                    # print(f"Matched scan {match_with.id} with {result.id}")
                    matched_scan_ids.add(result.id)
                    to_match.append(result)
                    base = base.join(result)
                tested.add(key)

    # find and rebase all the others that match it
    print(f"Base: {len(base.beacons)}")
    return base

    # then for each matched one, find any additional matches


class ScanTest(unittest.TestCase):
    def test_parse(self):
        test_input = """--- scanner 0 ---
        -1,-1,1
        -2,-2,2
        -3,-3,3
        -2,-3,1
        5,6,-4
        8,0,7
        
        --- scanner 1 ---
        -2,-3,2
        -2,-2,2
        -3,-3,3
        -2,-3,1
        5,6,-4
        8,0,7"""
        scans = list(Scan.parse(test_input.splitlines()))
        self.assertEqual(2, len(scans))
        self.assertEqual(6, len(scans[0].beacons))
        self.assertEqual(6, len(scans[1].beacons))
        print(scans[0])
        # get all the orientations
        os = scans[0].all_orientations
        print(len(os))

    def test_overlap(self):
        scans = list(Scan.parse(test_input1.splitlines()))
        self.assertEqual(5, len(scans))
        # find overlap between 0 and 1
        scans[0].intersect(scans[1])

    def test_join_scans(self):
        scans = list(Scan.parse(test_input1.splitlines()))
        join_scans(scans)

    def test_part_1(self):
        scans = list(Scan.parse(data.splitlines()))
        join_scans(scans)

    def test_distance(self):
        self.assertEqual(3621, Coord(1105, -1205, 1229).distance(Coord(-92, -2380, -20)))

    def test_part2_test(self):
        lines = part1_test_output.splitlines()
        scanners = [l for l in lines if l.startswith("Other")]
        coords: List[Coord] = [Coord(0, 0, 0)]
        for scanner in scanners:
            nums = utils.extractInts(scanner)
            coord = Coord(nums[0], nums[1], nums[2])
            coords.append(coord)

        dists = [a.distance(b) for a, b in combinations(coords, 2)]
        print(dists)
        # 11882 too low
        print(max(dists))
        self.assertEqual(3621, max(dists))

    def test_part2(self):
        lines = part1_output.splitlines()
        scanners = [l for l in lines if l.startswith("Other")]
        coords: List[Coord] = [Coord(0,0,0)]
        for scanner in scanners:
            nums = utils.extractInts(scanner)
            coord = Coord(nums[0], nums[1], nums[2])
            coords.append(coord)

        dists = [a.distance(b) for a, b in combinations(coords, 2)]
        print(dists)
        # 11882 too low
        print(max(dists))
