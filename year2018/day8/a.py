import logging
import os
import time
from collections import namedtuple
from functools import lru_cache

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


Node = namedtuple("Node", ["childs", "metadata"])


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(x) for x in f.readline().strip().split(" ")]


def sum_metadata(node: Node):
    return sum(node.metadata) + sum(sum_metadata(child) for child in node.childs)


def build_node(desc, idx=0):
    childs_qty, metadata_qty = desc[idx : idx + 2]
    idx += 2
    childs = []
    for _ in range(childs_qty):
        idx, child = build_node(desc, idx)
        childs.append(child)
    metadata = desc[idx : idx + metadata_qty]
    idx += metadata_qty
    return idx, Node(tuple(childs), tuple(metadata))


@lru_cache(maxsize=None)
def count_value(node: Node) -> int:
    if not node.childs:
        return sum(node.metadata)
    res = 0
    for ref in node.metadata:
        ref -= 1
        if ref < len(node.childs):
            res += count_value(node.childs[ref])
    return res


def main():
    desc = parse_input()
    idx, node = build_node(desc)
    logger.info(f"Res A {sum_metadata(node)}")
    logger.info(f"Res B {count_value(node)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
