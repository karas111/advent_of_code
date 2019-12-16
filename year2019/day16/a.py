import logging
import copy
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        return [int(c) for c in f.readline()]


PATTERN = [0, 1, 0, -1]


def create_pattern(n, tot_len):
    new_pattern = []
    which_digit = 0
    n_digit = 0
    i = 0
    while i < tot_len + 1:
        new_pattern.append(PATTERN[which_digit])
        i += 1
        n_digit += 1
        if n_digit == n:
            n_digit = 0
            which_digit = (which_digit + 1) % len(PATTERN)
    return new_pattern[1:]


def get_digit(x):
    return abs(x) % 10


def simulate(signal, n_simulation):
    for i in range(n_simulation):
        new_signal = []
        for j in range(len(signal)):
            new_patttern = create_pattern(j+1, len(signal))
            new_signal.append(get_digit(sum(x * p for x, p in zip(signal, new_patttern))))
        signal = new_signal
        logger.info('Phase finished after %d', i+1)
    return signal


def part_b(signal, n_simulation):
    offset = int(''.join(map(str, signal[:7])))
    offset -= len(signal)*10000//2
    logger.info('Offset %d', offset)
    signal = signal*(10000//2)
    logger.info('Mod signal length %d', len(signal))
    for n in range(n_simulation):
        for i in range(len(signal) - 2, -1, -1):
            signal[i] = signal[i+1] + signal[i]
        logger.info('Calculating phase %d', n)
    return [get_digit(x) for x in signal[offset: offset + 8]]


def main():
    signal = read_input()
    res = simulate(copy.copy(signal), n_simulation=100)
    logger.info('Result part a: %s', res[0:8])
    res = part_b(copy.copy(signal), 100)
    logger.info('Result part b: %s.', res)


if __name__ == "__main__":
    init_logging()
    main()
