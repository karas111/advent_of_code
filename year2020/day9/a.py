import logging
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(line.strip()) for line in f if line]


def find_not_matching(numbers, preambule=25):
    sums = {}

    def _add_to_sums(i, j):
        if numbers[i] != numbers[j]:
            _sum = numbers[i] + numbers[j]
            sums[_sum] = sums.get(_sum, 0) + 1

    def _remove_from_sums(i, j):
        if numbers[i] != numbers[j]:
            _sum = numbers[i] + numbers[j]
            sums[_sum] -= 1

    for i in range(preambule):
        for j in range(i, preambule):
            _add_to_sums(i, j)

    for i in range(preambule, len(numbers)):
        number_to_add = numbers[i]
        if not sums.get(number_to_add):
            return number_to_add
        for j in range(i + 1 - preambule, i):
            _add_to_sums(i, j)
            _remove_from_sums(i - preambule, j)

    raise ValueError("Not Found not matching")


def find_subsum(numbers, subsum):
    prefix_sums = []
    last_sum = 0
    for number in numbers:
        last_sum += number
        prefix_sums.append(last_sum)
    i, j = 0, 1
    while i < j and j < len(numbers):
        if i == 0:
            current_sum = prefix_sums[j]
        else:
            current_sum = prefix_sums[j] - prefix_sums[i - 1]
        if current_sum == subsum:
            return i, j
        elif current_sum < subsum:
            j += 1
        else:
            i += 1
    raise ValueError("Not found matching subsum")


def main():
    numbers = read_input()
    res_a = find_not_matching(numbers, preambule=25)
    logger.info(f"Res A={res_a}")
    i, j = find_subsum(numbers, res_a)
    logger.info(f"Indexes ({i} - {j}) sums to {sum(numbers[i:j+1])}")
    res_b = max(numbers[i : j + 1]) + min(numbers[i : j + 1])
    logger.info(f"Res B={res_b}")


if __name__ == "__main__":
    init_logging()
    main()
