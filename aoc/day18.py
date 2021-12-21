from __future__ import annotations

import math
import unittest
from dataclasses import dataclass
from itertools import permutations
from typing import List, Optional

from aocd import data


@dataclass
class Node:
    val: Optional[int] = None
    left: Optional[Node] = None
    right: Optional[Node] = None
    parent: Optional[Node] = None

    def depth(self):
        return 1 if self.parent is None else self.parent.depth() + 1

    def is_leaf(self) -> bool:
        return self.val is not None

    def right_leaf(self) -> Node:
        if self.is_leaf():
            return self
        return self.right.right_leaf()

    def left_leaf(self) -> Node:
        if self.is_leaf():
            return self
        return self.left.left_leaf()

    def find_left_parent(self) -> Optional[Node]:
        p = self
        while p:
            next_p = p.parent
            if next_p and next_p.right is p:
                return next_p.left
            p = next_p
        return None

    def find_right_parent(self) -> Optional[Node]:
        p = self
        while p:
            next_p = p.parent
            if next_p and next_p.left is p:
                return next_p.right
            p = next_p
        return None

    def find_left_num(self) -> Optional[Node]:
        p = self.find_left_parent()
        if p:
            return p.right_leaf()
        return None

    def find_right_num(self) -> Optional[Node]:
        p = self.find_right_parent()
        if p:
            return p.left_leaf()
        return None

    def explode(self, left_parent: bool) -> bool:
        if not self.left.is_leaf() and self.left.explode(left_parent=True):
            return True
        if not self.right.is_leaf() and self.right.explode(left_parent=False):
            return True
        if not self.is_leaf() and self.depth() > 4:
            left_node = self.find_left_num()
            right_node = self.find_right_num()
            if left_node:
                # add to the right num in left_pair
                left_node.val += self.left.val
            if right_node:
                right_node.val += self.right.val
            if left_parent:
                self.parent.left = Node(0, parent=self.parent)
            else:
                self.parent.right = Node(0, parent=self.parent)
            return True
        return False

    def split(self) -> bool:
        if self.is_leaf():
            if self.val > 9:
                self.left = Node(math.floor(self.val / 2), None, None, self)
                self.right = Node(math.ceil(self.val / 2), None, None, self)
                self.val = None
                return True
            else:
                return False
        return self.left.split() or self.right.split()

    def __str__(self):
        if self.is_leaf():
            return str(self.val)
        else:
            return f"[{self.left},{self.right}]"

    @classmethod
    def value(cls, val: int, parent: Optional[Node]):
        return Node(val, None, None, parent)

    def magnitude(self) -> int:
        if self.is_leaf():
            return self.val
        return self.left.magnitude() * 3 + self.right.magnitude() * 2


def parse(s: str) -> Node:
    stack: List = []
    buffer = ""
    for c in s:
        if c == "[":
            pass
        elif c == ",":
            if buffer:
                stack.append(Node.value(int(buffer), None))
                buffer = ""
        elif c == "]":
            if buffer:
                stack.append(Node.value(int(buffer), None))
                buffer = ""
            right = stack.pop()
            left = stack.pop()
            new_p = Node(None, left, right, None)
            left.parent = new_p
            right.parent = new_p
            stack.append(new_p)
        else:
            buffer += c

    return stack.pop()


def normalise(root: Node) -> Node:
    while True:
        exploded = root.explode(left_parent=True)
        if not exploded:
            if not root.split():
                return root


def add(left: Node, right: Node) -> Node:
    node = Node(None, left, right, None)
    left.parent = node
    right.parent = node
    return normalise(node)


def add_list(nodes: List[str]) -> Node:
    node = parse(nodes[0])
    for i in range(1, len(nodes)):
        node = add(node, parse(nodes[i]))
        node = normalise(node)
    return node


def max_pair(strs: List[str]) -> int:
    mag = 0
    for a, b in permutations(strs, 2):
        m = add(parse(a), parse(b)).magnitude()
        mag = max(mag, m)
    print(f"Max mag is {mag}")
    return mag


test_input = """[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"""


class MyTest(unittest.TestCase):
    def test_split(self):
        p = parse("[10,11]")
        p.split()
        self.assertEqual("[[5,5],11]", str(p))
        p.split()
        self.assertEqual("[[5,5],[5,6]]", str(p))

    def test_parse(self):
        for line in test_input.splitlines():
            with self.subTest(line):
                p = parse(line)
                self.assertEqual(line, str(p))

    def test_explode(self):
        self._explode("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]")
        self._explode("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]")
        self._explode("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
        self._explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
        self._explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

    def _explode(self, before: str, expected: str):
        with self.subTest(before):
            p = parse(before)
            self.assertTrue(p.explode(True))
            self.assertEqual(expected, str(p))

    def test_add(self):
        # [1,2] + [[3,4],5] becomes [[1,2],[[3,4],5]].
        p = add(parse("[1,2]"), parse("[[3,4],5]"))
        self.assertEqual("[[1,2],[[3,4],5]]", str(p))

    def test_normalise(self):
        p = add(parse("[[[[4,3],4],4],[7,[[8,4],9]]]"), parse("[1,1]"))
        print(p)
        self.assertEqual("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", str(p))

    def test_add_list(self):
        input1 = """[1,1]
[2,2]
[3,3]
[4,4]"""
        result = add_list(input1.splitlines())
        self.assertEqual("[[[[1,1],[2,2]],[3,3]],[4,4]]", str(result))

    def test_add_list2(self):
        input1 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""
        result = add_list(input1.splitlines())
        self.assertEqual("[[[[3,0],[5,3]],[4,4]],[5,5]]", str(result))

    def test_add_listN(self):
        input1 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
        result = add_list(input1.splitlines())
        self.assertEqual("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", str(result))

    def test_magnitude(self):
        self.assertEqual(143, parse("[[1,2],[[3,4],5]]").magnitude())

    def test_all(self):
        input1 = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

        node = add_list(input1.splitlines())
        self.assertEqual("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]", str(node))
        self.assertEqual(4140, node.magnitude())

    def test_part1(self):
        node = add_list(data.splitlines())
        print(node)
        print(node.magnitude())
        self.assertEqual(3494, node.magnitude())

    def test_part2_test(self):
        test_input1 = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
        self.assertEqual(3993, max_pair(test_input1.splitlines()))

    def test_part2(self):
        self.assertEqual(4712, max_pair(data.splitlines()))
