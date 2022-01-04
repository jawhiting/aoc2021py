import unittest
from operator import itemgetter
from typing import List, Iterator, Tuple, Dict, Set

import aocd


def convert(input: str) -> str:
    return "\n".join([to_code(line) for line in input.splitlines()])


def to_code(input: str) -> str:
    p = input.strip().split()
    if p[0] == "inp":
        return f"{p[1]} = input.pop(0)"
    if p[0] == "add":
        return f"{p[1]} += {p[2]}"
    if p[0] == "mul":
        return f"{p[1]} *= {p[2]}"
    if p[0] == "div":
        return f"{p[1]} = {p[1]} // {p[2]}"
    if p[0] == "mod":
        return f"{p[1]} %= {p[2]}"
    if p[0] == "eql":
        return f"{p[1]} = 1 if {p[1]} == {p[2]} else 0"


def template(input: List[int]) -> int:
    z = 0
    # Generated code goes here
    x = input.pop(0)
    x *= -1
    # Generated code ends
    return z


def generated_test_input1(input: List[int]) -> int:
    z = 0
    # Generated code goes here
    z = input.pop(0)
    x = input.pop(0)
    z *= 3
    z = 1 if z == x else 0
    # Generated code ends
    return z


def hand_part1(input: List[int]) -> int:
    z = 0
    w = input.pop(0)
    x = z % 26
    z = z // 1
    x += 11

    # First digit
    #

    pass


def generated_part1(input: List[int]) -> int:
    x = 0
    y = 0
    z = 0
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 1
    x += 11
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 6
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 1
    x += 13
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 14
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 1
    x += 15
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 14
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 26
    x += -8
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 10
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 1
    x += 13
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 9
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 1
    x += 15
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 12
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 26
    x += -11
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 8
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 26
    x += -4
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 13
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 26
    x += -15
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 12
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 1
    x += 14
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 6
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 1
    x += 14
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 9
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 26
    x += -1
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 26
    x += -8
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 4
    y *= x
    z += y
    w = input.pop(0)
    x *= 0
    x += z
    x %= 26
    z = z // 26
    x += -14
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 10
    y *= x
    z += y
    return z


vals = {
    1: (1, 11, 6),
    2: (1, 13, 14),
    3: (1, 15, 14),
    4: (26, -8, 10),
    5: (1, 13, 9),
    6: (1, 15, 12),
    7: (26, -11, 8),
    8: (26, -4, 13),
    9: (26, -15, 12),
    10: (1, 14, 6),
    11: (1, 14, 9),
    12: (26, -1, 15),
    13: (26, -8, 4),
    14: (26, -14, 10)
}


def find_inputs(digit: int, target: Set[int]) -> Iterator[Tuple[int, int, int]]:
    for z in range(26*26*26*26, -1, -1):
        for w in range(9, 0, -1):
            r = calc_digit(z, w, digit)
            if r in target:
                yield z,w,r


def calc_digit(z: int, w: int, digit: int) -> int:
    zdiv = vals[digit][0]
    xinc = vals[digit][1]
    yinc = vals[digit][2]
    x = 0
    y = 0
    x *= 0
    x += z
    x %= 26
    z = z // zdiv
    x += xinc
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += yinc
    y *= x
    z += y
    return z


def search() -> int:
    count = 0
    for i in range(99999999999999, 11111111111111, -1):
        input = create_input(i)
        if input:
            result = generated_part1(input)
            print(f"{i} Result: {result}")
            if result == 0:
                print(f"{i} Result: {result}")
                break


def create_input(input: int) -> List[int]:
    i = input
    result: List[int] = []
    while i:
        digit = i % 10
        if digit == 0:
            return None
        result.insert(0, digit)
        i //= 10
    return result


class TestConversion(unittest.TestCase):
    def test_convert_input1(self):
        test_input = """inp z
inp x
mul z 3
eql z x"""
        print(convert(test_input))

    def test_generated_1(self):
        self.assertEqual(1, generated_test_input1([3, 9]))
        self.assertEqual(0, generated_test_input1([3, 10]))

    def test_generate_part1(self):
        print(convert(aocd.data))

    def test_create_input(self):
        self.assertEqual([1, 2, 3], create_input(123))

    def test_part1(self):
        for i in range(1000):
            inp = create_input(99394899891971 - i)
            if inp:
                print(generated_part1(inp))

    def test_brute_force(self):
        search()

    def test_min_14(self):
        # 14 0 -> 0
        # 15 1 -> 0
        # 16 2 -> 0
        # 17 3 -> 0
        # 18 4 -> 0
        # 19 5 -> 0
        # 20 6 -> 0
        # 21 7 -> 0
        # 22 8 -> 0
        # 23 9 -> 0
        for i in range(30):
            for d in range(10):
                if calc_digit(i, d, 14) == 0:
                    print(f"{i} {d} -> {calc_digit(i, d, 14)}")
        for i in find_inputs(14, 0):
            print(i)

    def test_find_part1(self):
        inputs: Dict[int, Set[Tuple[int, int, int]]] = {15: {(0,0,0)}}
        for d in range(14, 0, -1):
            targets = set([i[0] for i in inputs[d+1]])
            inputs[d] = set(find_inputs(d, targets))
        # print(inputs)
        # Now build the largest number starting from left
        result = ""
        next_target = 0
        for d in range(1, 15):
            print(f"Digit: {d} options:")
            # for v in set(inputs[d]):
            #     print(f"{v}")
            # # find highest digit then its target
            if not inputs[d]:
                print("Digit: 9 (no difference)")
                result += "9"
            else:
                # pick the highest target
                candidates = [t for t in inputs[d] if t[0] == next_target]
                print(candidates)
                # Now find the highest digit
                highest_digit = max(candidates, key=itemgetter(1))
                print(f"Digit: {highest_digit}")
                next_target = highest_digit[2]
                result += str(highest_digit[1])
        print(result)
        self.assertEqual(99394899891971, result)
        #91191199991999
        #99399959391979 too high

    def test_find_part2(self):
        target = {0}
        inputs: Dict[int, Set[Tuple[int, int, int]]] = {15: {(0,0,0)}}
        for d in range(14, 0, -1):
            targets = set([i[0] for i in inputs[d+1]])
            inputs[d] = set(find_inputs(d, targets))
        # print(inputs)
        # Now build the largest number starting from left
        result = ""
        next_target = 0
        for d in range(1, 15):
            print(f"Digit: {d} options:")
            # for v in set(inputs[d]):
            #     print(f"{v}")
            # # find highest digit then its target
            if not inputs[d]:
                print("Digit: 1 (no difference)")
                result += "1"
            else:
                # pick the highest target
                candidates = [t for t in inputs[d] if t[0] == next_target]
                print(candidates)
                # Now find the highest digit
                lowest_digit = min(candidates, key=itemgetter(1))
                print(f"Digit: {lowest_digit}")
                next_target = lowest_digit[2]
                result += str(lowest_digit[1])
        print(result)
        self.assertEqual(92171126131911, result)
        #91191199991999
        #99399959391979 too high