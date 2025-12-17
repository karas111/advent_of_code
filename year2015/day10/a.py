import logging

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def transform(seq: str, n: int) -> str:
    for _ in range(n):
        c = seq[0]
        count = 1
        res = ""
        for idx in range(1, len(seq)):
            if seq[idx] != c:
                res += f"{count}{c}"
                count = 1
                c = seq[idx]
            else:
                count += 1
        res += f"{count}{c}"

        seq = res
    return seq


def main():
    seq = "1113122113"
    res = transform(seq, 40)
    logger.info("Res a: %s", len(res))
    res = transform(res, 10)
    logger.info("Res b: %s", len(res))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
