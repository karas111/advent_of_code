import logging
import time

from year2017.day17.a import LinkedList
from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def creatr_circle(seed):
    nodes = [LinkedList(i) for i in range(1, seed + 1)]
    for i in range(len(nodes) - 1):
        nodes[i].right = nodes[i + 1]
    nodes[-1].right = nodes[0]
    return nodes[0]


def main():
    seed = 3001330
    # seed = 5
    x = list(range(seed))
    offset = 0
    while len(x) > 1:
        next_offset = (len(x) - offset) % 2
        x = x[offset::2]
        offset = next_offset

    logger.info(f"Res A {x[0] + 1}")

    current = creatr_circle(seed)
    prev_to_remove = current
    for i in range(seed // 2 - 1):
        prev_to_remove = prev_to_remove.right
    for i in range(seed - 1):
        prev_to_remove.right = prev_to_remove.right.right
        if (i + seed) % 2 == 1:
            prev_to_remove = prev_to_remove.right
    logger.info(f"Res B {prev_to_remove.value}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
