import math
from collections import defaultdict
from dataclasses import dataclass
from statistics import median
from typing import List, Callable, Set, Dict, Optional

from utils import extractInts
from aocd import data

test_input = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

open = "([{<"
close = ")]}>"
scores = [3, 57, 1197, 25137]
completion = [1,2,3,4]

def is_error(chunk: str) -> Optional[int]:
    """Returns None or the unbalanced char"""
    stack: List[int] = []
    for c in chunk:
        if c in open:
            # open
            stack.append(open.index(c))
        else:
            # close
            expected_index = stack.pop()
            if close[expected_index] != c:
                # Syntax error
                return close.index(c)


def is_error2(chunk: str) -> int:
    """Returns None or the unbalanced char"""
    stack: List[int] = []
    for c in chunk:
        if c in open:
            # open
            stack.append(open.index(c))
        else:
            # close
            expected_index = stack.pop()
            if close[expected_index] != c:
                # Syntax error
                return 0
    # now return the remaining stack
    return completion_score(stack)

def completion_score(stack: List[str]) -> int:
    score = 0
    while stack:
        next_score = stack.pop()
        score = score * 5 + completion[next_score]
    return score


def part2(lines: List[str]):
    s = [e for line in lines if (e := is_error2(line)) > 0]
    print(s)
    print(median(s))

def part1(lines: List[str]):
    s = [scores[e] for line in lines if (e := is_error(line)) is not None]
    print(f"Scores: {s}")
    print(f"Total: {sum(s)}")


if __name__ == "__main__":
    test_lines = test_input.splitlines()

    # print(is_error("[[<[([]))<([[{}[[()]]]"))
    # print(is_error("[({(<(())[]>[[{[]{<()<>>"))

    print(is_error2("<{([{{}}[<[[[<>{}]]]>[]]"))

    part1(test_lines)
    part1(data.splitlines())
    part2(test_lines)
    part2(data.splitlines())
