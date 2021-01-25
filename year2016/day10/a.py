import logging
import os
import re
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    init_val = {}
    graph = {}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("bot"):
                node, low_bot, low, high_bot, high = re.match(
                    r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)",
                    line,
                ).groups()
                graph[int(node)] = (
                    int(low),
                    low_bot == "bot",
                    int(high),
                    high_bot == "bot",
                )
            elif line.startswith("value"):
                value, node = re.match(r"value (\d+) goes to bot (\d+)", line).groups()
                init_val.setdefault(int(node), []).append(int(value))

    return init_val, graph


def run_bots(init_val, graph):
    queue = [k for k, v in init_val.items() if len(v) >= 2]
    outputs = {}
    while queue:
        bot = queue.pop()
        low, high = sorted(init_val[bot])
        if low == 17 and high == 61:
            logger.info(f"Res A {bot}")
        low_out, low_bot, high_out, high_bot = graph[bot]
        for value, dest, is_bot in [
            (low, low_out, low_bot),
            (high, high_out, high_bot),
        ]:
            if is_bot:
                init_val.setdefault(dest, []).append(value)
                if len(init_val[dest]) >= 2:
                    queue.append(dest)
            else:
                outputs.setdefault(dest, []).append(value)
            init_val[bot] = []
    return outputs


def main():
    init_val, graph = parse_input()
    outputs = run_bots(init_val, graph)
    logger.info(f"Res B {outputs[0][0] * outputs[1][0] * outputs[2][0]}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
