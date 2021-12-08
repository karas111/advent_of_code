import logging
import os
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

UNIQUE_SEGMENTS = {2: 1, 4: 4, 3: 7, 7: 8}


class Instruction:
    def __init__(self, singals: List[str], output: List[str]) -> None:
        self.signals = singals
        self.output = output

    def __repr__(self) -> str:
        return f"{self.signals} | {self.output}"


def read_input() -> List[Instruction]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        res = []
        for line in f:
            if not line:
                continue
            signals, output = line.strip().split(" | ")
            res.append(
                Instruction(singals=signals.split(" "), output=output.split(" "))
            )
    return res


def find_mapping(signals: List[str]):
    signals = [set(signal) for signal in signals]
    mapping = {8: set("abcdefg")}
    for signal in signals:
        if len(signal) == 2:
            mapping[1] = signal
        elif len(signal) == 3:
            mapping[7] = signal
        elif len(signal) == 4:
            mapping[4] = signal
    for signal in signals:
        if len(signal) == 6 and len(signal | mapping[1]) == 7:
            mapping[6] = signal
    segment_c = (mapping[8] - mapping[6]).pop()
    segment_f = (mapping[1] - {segment_c}).pop()
    for signal in signals:
        if len(signal) == 5 and segment_c not in signal:
            mapping[5] = signal
    segment_e = (mapping[8] - mapping[5] - {segment_c}).pop()
    for signal in signals:
        if len(signal) == 6 and segment_e not in signal:
            mapping[9] = signal
    for signal in signals:
        if len(signal) == 5:
            if segment_e in signal:
                mapping[2] = signal
            elif segment_f in signal and signal != mapping[5]:
                mapping[3] = signal
    for signal in signals:
        if signal not in mapping.values():
            mapping[0] = signal
    return mapping


def decode_inst(inst: Instruction) -> int:
    mapping = find_mapping(inst.signals)
    mapping = {frozenset(signal): number for number, signal in mapping.items()}
    res = 0
    for signal in inst.output:
        res = res * 10 + mapping[frozenset(signal)]
    return res


def find_sum(instructions: List[Instruction]) -> int:
    return sum(decode_inst(inst) for inst in instructions)


def count_unique(instructions: List[Instruction]) -> int:
    res = 0
    for inst in instructions:
        for output_number in inst.output:
            if len(output_number) in UNIQUE_SEGMENTS:
                res += 1
    return res


def main():
    instructions = read_input()
    logger.info(f"Res a {count_unique(instructions)}")
    tot_sum = find_sum(instructions)
    logger.info(f"Res b {tot_sum}")


if __name__ == "__main__":
    init_logging()
    main()
