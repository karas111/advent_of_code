from collections import defaultdict
import logging
import os
from typing import Dict, List, Tuple, Optional

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "test2.txt"


class Node:
    def __init__(self) -> None:
        self.parent: Optional[Knot] = None
        self.depth = 0

    @staticmethod
    def parse(repr_str: str) -> "Node":
        node, _, _ = Node._parse(repr_str)
        node.recalculate_depth()
        return node

    @staticmethod
    def _parse(
        repr_str: str, idx: int = 0, last_leaf: "Node" = None
    ) -> Tuple["Node", int, "Leaf"]:
        if repr_str[idx] == "[":
            idx += 1
            left, idx, last_leaf = Node._parse(repr_str, idx, last_leaf)
            assert repr_str[idx] == ","
            idx += 1
            right, idx, last_leaf = Node._parse(repr_str, idx, last_leaf)
            node = Knot(left, right)
            assert repr_str[idx] == "]"
            idx += 1
            return node, idx, last_leaf
        elif repr_str[idx] in "0123456789":
            node = Leaf(int(repr_str[idx]))
            node.left_leaf = last_leaf
            if last_leaf:
                last_leaf.right_leaf = node
            last_leaf = node
            idx += 1
            return node, idx, last_leaf
        raise ValueError("could not parse")

    def recalculate_depth(self):
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1

    def explode(self) -> bool:
        return False

    def split(self) -> bool:
        return False

    def reduce(self):
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            return

    def add(self, other):
        new_node = Knot(self, other)
        left_leaf, right_leaf = (
            self.get_outermost_leaf(left=False),
            other.get_outermost_leaf(left=True),
        )
        left_leaf.right_leaf = right_leaf
        right_leaf.left_leaf = left_leaf
        new_node.recalculate_depth()
        new_node.reduce()
        return new_node


class Knot(Node):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__()
        self.left = left
        self.right = right
        left.parent = right.parent = self

    def __repr__(self) -> str:
        return f"[{self.left},{self.right}]"

    def recalculate_depth(self):
        super().recalculate_depth()
        self.left.recalculate_depth()
        self.right.recalculate_depth()

    def need_reduce(self) -> bool:
        return self.depth >= 4

    def replace(self, node: Node, new_node: Node):
        new_node.parent = self
        if self.left == node:
            self.left = new_node
        elif self.right == node:
            self.right = new_node
        else:
            raise ValueError(f"Node {node} is not one of childs of {self}")

    def explode(self) -> bool:
        if self.left.explode():
            return True
        if self.need_reduce():
            assert isinstance(self.left, Leaf)
            assert isinstance(self.right, Leaf)
            new_node = Leaf(0)
            left_to_inc = self.left.left_leaf
            if left_to_inc:
                left_to_inc.val += self.left.val
                left_to_inc.right_leaf = new_node
                new_node.left_leaf = left_to_inc
            right_to_inc = self.right.right_leaf
            if right_to_inc:
                right_to_inc.val += self.right.val
                right_to_inc.left_leaf = new_node
                new_node.right_leaf = right_to_inc
            self.parent.replace(self, new_node)
            new_node.recalculate_depth()
            return True
        return self.right.explode()

    def split(self) -> bool:
        if self.left.split():
            return True
        return self.right.split()

    def get_outermost_leaf(self, left=True) -> "Leaf":
        if left:
            return self.left.get_outermost_leaf(left)
        else:
            return self.right.get_outermost_leaf(left)


class Leaf(Node):
    def __init__(self, val: int) -> None:
        super().__init__()
        self.val = val
        self.left_leaf = None
        self.right_leaf = None

    def __repr__(self) -> str:
        return f"{self.val}"

    def need_reduce(self) -> bool:
        return self.val >= 10

    def split(self):
        if self.need_reduce():
            left = Leaf(self.val // 2)
            right = Leaf(self.val - left.val)
            new_node = Knot(left, right)
            left.left_leaf = self.left_leaf
            left.right_leaf = right
            right.left_leaf = left
            right.right_leaf = self.right_leaf
            self.parent.replace(self, new_node)
            new_node.recalculate_depth()
            return True
        return False

    def get_outermost_leaf(self, left=True) -> "Leaf":
        return self


def read_input() -> List[Node]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        res = []
        for line in f:
            if not line:
                continue
            node = Node.parse(line.strip())
            node.recalculate_depth()
            res.append(node)
        return res


def sum_nodes(nodes: List[Node]) -> Node:
    res = nodes[0]
    for node in nodes[1:]:
        res = res.add(node)
        logger.info(f"\n{res}")
    return res


def main():
    nodes = read_input()
    node = sum_nodes(nodes)
    logger.info(f"Res a {node}")


if __name__ == "__main__":
    init_logging()
    main()
