import copy
import logging
import re
import os
import time
from collections import Counter
from typing import Tuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    graph = {}
    weights = {}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                if " -> " in line:
                    node_weight, childs = line.strip().split(" -> ")
                    childs = childs.split(", ")
                else:
                    node_weight = line
                    childs = []
                node, weight = re.match(r"(\w+) \((\d+)\)", node_weight).groups()
                graph[node] = childs
                weights[node] = int(weight)
    return graph, weights


def rev_graph(graph):
    res = {n: [] for n in graph}
    for node, childs in graph.items():
        for child in childs:
            res[child].append(node)
    return res


def get_weights(graph, weights, node, summed_weights=None):
    if summed_weights is None:
        summed_weights = {}
    childs_weights = {child: get_weights(graph, weights, child, summed_weights) for child in graph[node]}
    if len(set(childs_weights.values())) > 1:
        correct_weight = next(w for w, count in Counter(childs_weights.values()).items() if count > 1)
        for child, w in childs_weights.items():
            if w != correct_weight:
                logger.info(f"Correct weight for node {child} is {weights[child] - w + correct_weight}")
        raise ValueError(f"Not balanced for {node} childs {graph[node]}, {childs_weights}")
    summed_weights[node] = weights[node] + sum(childs_weights.values())
    return summed_weights[node]


def main():
    graph, weights = parse_input()
    rgraph = rev_graph(graph)
    root = next(k for k, v in rgraph.items() if len(v) == 0)
    logger.info(f"Res A {root}")
    get_weights(graph, weights, root)
    # logger.info(f"Res B {ju}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
