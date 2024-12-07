import logging
import os
import re
from typing import Iterable

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Instruction = tuple[int, list[int]]


def read_input() -> Iterable[Instruction]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        pattern = r"\d+"
        instructions = [
            [int(x) for x in re.findall(pattern, line.strip())]
            for line in f
            if line.strip()
        ]
        return [(result, params) for result, *params in instructions]


def is_valid(inst: Instruction, concatenation_enabled) -> bool:
    result, params = inst
    if len(params) == 1:
        return result == params[0]
    *rest_params, last_param = params
    if last_param > result:
        return False
    if result % last_param == 0 and is_valid(
        (result // last_param, rest_params), concatenation_enabled
    ):
        return True
    if is_valid((result - last_param, rest_params), concatenation_enabled):
        return True
    if not concatenation_enabled:
        return False
    result_str, last_param_str = str(result), str(last_param)
    return result_str.endswith(last_param_str) and is_valid(
        (int(result_str[: -len(last_param_str)] or 0), rest_params),
        concatenation_enabled,
    )


def main():
    instructions = list(read_input())

    valid_insts = [
        inst for inst in instructions if is_valid(inst, concatenation_enabled=False)
    ]
    logger.info("Res a %s", sum(inst[0] for inst in valid_insts))
    valid_insts = [
        inst for inst in instructions if is_valid(inst, concatenation_enabled=True)
    ]
    logger.info("Res b %s", sum(inst[0] for inst in valid_insts))


if __name__ == "__main__":
    init_logging()
    main()
