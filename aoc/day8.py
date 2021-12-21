from collections import defaultdict
from typing import List, Callable, Set, Dict

from utils import extractInts
from aocd import data

test_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


input = data

count_to_digits : Dict[int, Set[int]] = {
    2 : {1},
    3 : {7},
    4 : {4},
    5 : {2, 3, 5},
    6 : {0, 6, 9},
    7 : {8},
}

wire_to_digits : Dict[int, Set[int]] = {
    1 : {0,    2, 3,    5, 6, 7, 8, 9},
    2 : {0,          4, 5, 6,    8, 9},
    3 : {0, 1, 2, 3, 4,       7, 8, 9},
    4 : {      2, 3, 4, 5, 6,    8, 9},
    5 : {0,    2,          6,    8   },
    6 : {0, 1,    3, 4, 5, 6, 7, 8, 9},
    7 : {0,    2, 3,    5, 6,    8, 9}
}

digit_to_wires : Dict[int, Set[int]] = {
    1 : {      3,       6   },
    7 : {1,    3,       6   },
    4 : {   2, 3, 4,    6   },
    # 5 wires
    2 : {1,    3, 4, 5,    7},
    3 : {1,    3, 4,    6, 7},
    5 : {1, 2,    4,    6, 7},
    # 6 wires
    0 : {1, 2, 3,    5, 6, 7},
    6 : {1, 2,    4, 5, 6, 7},
    9 : {1, 2, 3, 4,    6, 7},

    # 7 wires
    8 : {1, 2, 3, 4, 5, 6, 7},
}

test_simple = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
#                  8            2         7     9            4          1


def solve(inputs: List[Set[str]], outputs: List[Set[str]]) -> int:
    # Wire 1 is (7-1) -> d
    # Digit 9 is (4 intersect 6-count) == 4
    # Wire 5 is (8-9) -> g
    # Digit 2 is 5wire with Wire 5 ->
    # Digit 5 is 5-count intersect digit1 == 1

    digit1 = with_length(inputs, 2)[0]
    digit4 = with_length(inputs, 4)[0]
    digit7 = with_length(inputs, 3)[0]
    digit8 = with_length(inputs, 7)[0]
    inputs.remove(digit1)
    inputs.remove(digit4)
    inputs.remove(digit7)
    inputs.remove(digit8)

    # 1 intersect 3 is 2
    digit3 = find_match(inputs, 5, digit1, 2)
    inputs.remove(digit3)

    # 4 intersect 5 is 3
    digit5 = find_match(inputs, 5, digit4, 3)
    inputs.remove(digit5)

    # 4 intersect 2 is 2
    digit2 = find_match(inputs, 5, digit4, 2)
    inputs.remove(digit2)

    # Given 1 we can find 6 by 1 intersect 6wire == 1
    digit6 = find_match(inputs, 6, digit1, 1)
    inputs.remove(digit6)

    digit9 = find_match(inputs, 6, digit4, 4)
    inputs.remove(digit9)

    digit0 = find_match(inputs, 6, digit4, 3)
    inputs.remove(digit0)




    mappings = [digit0,
                digit1,
                digit2,
                digit3,
                digit4,
                digit5,
                digit6,
                digit7,
                digit8,
                digit9,
                ]
    print(f"Found mappings: {mappings}")
    result = 0
    for o in outputs:
        mapped = mappings.index(o)
        result = result * 10 + mapped
        print(f"Output: {o} is digit: {mappings.index(o)}")


    return result


def find_match(inputs: List[Set[str]], length: int, digit: Set[str], target: int):
    candidates = with_length(inputs, length)
    matched = [d for d in candidates if intersect(d, digit) == target]
    if len(matched) == 1:
        return matched[0]
    raise ValueError


def intersect(a: Set[str], b: Set[str]) -> int:
    return len(a.intersection(b))


def with_length(inputs: List[Set[str]], length: int) -> List[Set[str]]:
    return [d for d in inputs if len(d) == length]


def part1(lines: List[str]):
    segment_count = defaultdict(int)
    for l in lines:
        io = l.split("|")
        for o in io[1].split():
            segment_count[len(o)] += 1
    print(segment_count)
    # 1 4 7 8
    # 2 4 3 7
    print(segment_count[2] + segment_count[4] + segment_count[3] + segment_count[7])


def part2(lines: List[str]):
    overall_result = 0
    for l in lines:
        try:
            io = l.split("|")
            inputs = io[0].split()
            outputs = io[1].split()
            input_sets = [to_set(i) for i in inputs]
            output_sets = [to_set(i) for i in outputs]
            result = solve(input_sets, output_sets)
            print(f"Result is {result}")
            overall_result += result
        except Exception as e:
            print(f"Got exception for line: {l}")
            raise

    print(f"Overall result is: {overall_result}")

def to_set(string: str) -> Set[str]:
    return {c for c in string}

bug = "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg"
bug2 = "fcdeba edcbag decab adcefg acdfb gdcfb acf fabe fa eacfgbd | aefb cfa acf cdabf"
if __name__ == "__main__":
    # part1(test_input.splitlines())
    # part1(input.splitlines())
    # part2(test_simple.splitlines())
    # part2(test_input.splitlines())
    part2(input.splitlines())
    # part2(bug2.splitlines())
    # part2(input)
    # 984915 too high

