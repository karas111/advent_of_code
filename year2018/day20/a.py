import logging
import os
import copy
import time
from collections import deque

# import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

MOVE_VEC = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline()[1:-1]


def create_graph(regex):
    branches_start_stack = []
    branches_end_stack = []
    idx = 0
    current_posns = {(0, 0)}
    graph = {(0, 0): set()}
    while idx < len(regex):
        symb = regex[idx]
        if symb == "(":
            branches_start_stack.append(copy.copy(current_posns))
            branches_end_stack.append(set())
        elif symb == "|":
            branches_end_stack[-1] = copy.copy(current_posns) | branches_end_stack[-1]
            current_posns = copy.copy(branches_start_stack[-1])
        elif symb == ")":
            current_posns = current_posns | branches_end_stack.pop()
            branches_start_stack.pop()
        elif symb in MOVE_VEC:
            dx, dy = MOVE_VEC[symb]
            new_current_pos = set()
            for pos in current_posns:
                new_pos = (pos[0] + dx, pos[1] + dy)
                new_current_pos.add(new_pos)
                graph[pos].add(new_pos)
                graph.setdefault(new_pos, set()).add(pos)
            current_posns = new_current_pos
        idx += 1
    return graph


def dfs(graph, start=(0, 0)):
    queue = deque([(start, 0)])
    res = {}
    while queue:
        node, deph = queue.popleft()
        if node in res:
            continue
        res[node] = deph
        for other in graph[node]:
            queue.append((other, deph + 1))
    return res


def main():
    regexes = [
        "WNE",
        "ENWWW(NEEE|SSE(EE|N))",
        "ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN",
        "ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))",
        "WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))",
    ]
    for regex in regexes:
        graph = create_graph(regex)
        res_a = dfs(graph)
        logger.info(f"Res A for {regex} is {max(res_a.values())}")
    regex = parse_input()
    graph = create_graph(regex)
    res_a = dfs(graph)
    logger.info(f"Res A is {max(res_a.values())}")
    res_b = [x for x in res_a.values() if x >= 1000]
    logger.info(f"Res B is {len(res_b)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
