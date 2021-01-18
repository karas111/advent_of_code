import logging
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def generator(x, mult, mod, mod_res=1):
    while True:
        x = (x * mult) % mod
        if x % mod_res == 0:
            yield x & (0xFFFF)


def part_a(a, b, mod_a, mod_b, max_iter):
    gen_mod = 2147483647
    gen_a = generator(a, 16807, gen_mod, mod_a)
    gen_b = generator(b, 48271, gen_mod, mod_b)
    return sum(next(gen_a) == next(gen_b) for i in range(max_iter))


def main():
    a, b = 634, 301
    # a, b = 65, 8921
    logger.info(f"Res A {part_a(a, b, 1, 1, int(4e7))}")
    logger.info(f"Res B {part_a(a, b, 4, 8, int(5e6))}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
