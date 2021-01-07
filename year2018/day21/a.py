import logging
import time

from year2019.utils import init_logging

# from year2018.day19.day19a import read_input, execute_program

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def program(part_b):
    visited = set()
    x3, x4 = 0, 0
    last_x3 = None
    while (x3, x4) not in visited:
        visited.add((x3, x4))
        last_x3 = x3
        x4 = x3 | 65536
        x3 = 10649702
        while True:
            x3 += x4 & 255
            x3 = x3 & 16777215
            x3 *= 65899
            x3 = x3 & 16777215
            if x4 < 256:
                break
            x4 = x4 // 256
        if not part_b:
            return x3
    return last_x3


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    logger.info(f"Res A {program(False)}")
    logger.info(f"Res B {program(True)}")
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
    # program, ip = read_input(os.path.join(os.path.dirname(__file__), INPUT_FILE))
    # execute_program(program, ip, registers=[0]*6)
