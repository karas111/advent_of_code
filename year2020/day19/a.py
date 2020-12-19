import logging
import os
import time
from typing import Dict, List, Tuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Rule:
    def __init__(self, idx) -> None:
        self.idx = idx

    def match_start(self, line: str, rule_set: Dict[int, "Rule"]):
        raise NotImplementedError()

    def final_match(self, line: str, rule_set) -> bool:
        for res in self.match_start(line, rule_set):
            if res == "":
                return True
        return False


class LetterRule(Rule):
    def __init__(self, idx, letter) -> None:
        super().__init__(idx)
        self.letter = letter

    def match_start(self, line: str, rule_set: Dict[int, "Rule"]):
        if line and line[0] == self.letter:
            yield line[1:]


class MultiRule(Rule):
    def __init__(self, idx, subrules: List[List[int]]) -> None:
        super().__init__(idx)
        self.subrules = subrules

    def match_start(self, line: str, rule_set: Dict[int, "Rule"]):
        for subrule in self.subrules:
            for res in self.check_subrule(line, subrule, rule_set):
                yield res

    def check_subrule(self, line: str, subrule: List[int], rule_set: Dict[int, "Rule"]):
        if not subrule:
            yield line
            return
        rule = rule_set[subrule[0]]
        for subline in rule.match_start(line, rule_set):
            for x in self.check_subrule(subline, subrule[1:], rule_set):
                yield x


def read_input() -> Tuple[List[Rule], List[str]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        content = f.read().strip()
    rules, lines = content.split("\n\n")
    lines = lines.split("\n")
    rules = [parse_rule(line) for line in rules.split("\n")]
    rules = {rule.idx: rule for rule in rules}
    return rules, lines


def parse_rule(line: str) -> Rule:
    idx, right = line.split(": ")
    right = right.strip('"')
    if right.isalpha():
        return LetterRule(int(idx), right)
    subrules = [[int(x) for x in subrule.split(" ")] for subrule in right.split(" | ")]
    return MultiRule(int(idx), subrules)


def main():
    rules, lines = read_input()
    rule0 = rules[0]
    res = [rule0.final_match(line, rules) for line in lines]
    logger.info(f"Matching lines, {sum(res)}")

    rules[8] = MultiRule(8, [[42], [42, 8]])
    rules[11] = MultiRule(11, [[42, 31], [42, 11, 31]])
    res = [rule0.final_match(line, rules) for line in lines]
    logger.info(f"Matching lines, {sum(res)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
