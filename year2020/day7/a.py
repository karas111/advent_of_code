from collections import namedtuple
import logging
import os
import re

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

Node = namedtuple("Node", ["name", "qty"])

INPUT_FILE = "input.txt"


def read_graph():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        lines = [line.strip()[:-1] for line in f if line]
    graph = {}
    for line in lines:
        root, childs = line.split(" bags contain ")
        childs = [re.sub(" bags| bag", "", child) for child in childs.split(", ")]
        childs = [child for child in childs if child != "no other"]

        def parse_child(child):
            child = child.split(" ", maxsplit=1)
            return Node(child[1], int(child[0]))

        childs = [parse_child(child) for child in childs]
        graph[root] = childs
    return graph


def revert_graph(graph):
    new_graph = {}
    for root, childs in graph.items():
        for child in childs:
            new_graph.setdefault(child.name, []).append(root)
    return new_graph


def get_all_reachable(graph, start):
    visited = set()
    queue = [start]
    while queue:
        node = queue.pop()
        if node in visited:
            pass
        visited.add(node)
        queue = queue + graph.get(node, [])
    return visited


def get_total_bags(graph, start, cached=None):
    if cached is None:
        cached = {}
    if start not in cached:
        cached[start] = (
            sum(
                get_total_bags(graph, child.name, cached) * child.qty
                for child in graph[start]
            )
            + 1
        )
    return cached[start]


def main():
    graph = read_graph()
    # logger.info(f"Graph: {graph}")
    rev_graph = revert_graph(graph)
    # logger.info(f"Rev Graph: {rev_graph}")
    all_reacheable = get_all_reachable(rev_graph, "shiny gold")
    logger.info(f"All reacheable {all_reacheable}\nres A = {len(all_reacheable) - 1}")
    logger.info(f"Total bags {get_total_bags(graph, 'shiny gold') - 1}")


if __name__ == "__main__":
    init_logging()
    main()
