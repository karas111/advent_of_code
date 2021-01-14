import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


MOVE_VEC = {
    "n": (0, -1),
    "s": (0, 1),
    "se": (1, 0),
    "nw": (-1, 0),
    "ne": (1, -1),
    "sw": (-1, 1),
}


def parse_input():
    graph = {}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f.readlines():
            if line:
                node, neighbours = line.strip().split(" <-> ")
                graph[int(node)] = [int(n) for n in neighbours.split(", ")]
    return graph


def find_component(graph, start):
    component = set()
    queue = [start]
    while queue:
        node = queue.pop()
        component.add(node)
        for neighbour in graph[node]:
            if neighbour not in component:
                queue.append(neighbour)
    return component


def find_all_components(graph):
    seen = set()
    components = []
    for node in graph:
        if node not in seen:
            component = find_component(graph, node)
            seen = seen | component
            components.append(component)
    return components


def main():
    graph = parse_input()
    component = find_component(graph, 0)
    logger.info(f"Res A {len(component)}")
    components = find_all_components(graph)
    logger.info(f"Res B {len(components)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
