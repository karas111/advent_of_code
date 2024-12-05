import logging
import os
import re
from collections import defaultdict
from typing import Callable

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Graph = dict[int, list[int]]
Instruction = list[int]


def read_input() -> tuple[Graph, list[Instruction]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        graph = defaultdict(set)
        while line := f.readline().strip():
            x, y = re.match(r"(\d+)\|(\d+)", line).groups()
            graph[int(x)].add(int(y))
        instructions = []
        while line := f.readline().strip():
            instructions.append([int(x) for x in re.findall(r"\d+", line)])
        return graph, instructions


def check_instruction(instruction: Instruction, graph: Graph) -> bool:
    return all(y in graph[x] for x, y in zip(instruction, instruction[1:]))


def count_score(
    instructions: list[Instruction], filter_fn: Callable[[Instruction], bool]
) -> int:
    return sum(inst[len(inst) // 2] for inst in instructions if filter_fn(inst))


def fix_instr(instr: Instruction, graph: Graph) -> Instruction:
    pages_pos = {
        page: sum(other_page in graph[page] for other_page in instr) for page in instr
    }
    return [k for k, _ in sorted(pages_pos.items(), key=lambda x: x[1], reverse=True)]


def main():
    graph, instrs = read_input()
    res_a = count_score(instrs, lambda inst: check_instruction(inst, graph))
    logger.info("Res a %s", res_a)
    fixed_instr = [
        fix_instr(inst, graph) for inst in instrs if not check_instruction(inst, graph)
    ]
    res_b = count_score(fixed_instr, lambda _: True)
    logger.info("Res b %s", res_b)


if __name__ == "__main__":
    init_logging()
    main()
