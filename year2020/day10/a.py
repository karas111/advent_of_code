import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__) 

INPUT_FILE = "input.txt"


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(line.strip()) for line in f if line]


def create_diffs(adapters):
    res = []
    for i in range(len(adapters) -1):
        res.append(adapters[i+1] - adapters[i])
    return res


def find_ones(diffs):
    res = []
    i = 0
    for diff in diffs:
        if diff == 1:
            i += 1
        else:
            if i != 0:
                res.append(i)
            i = 0
    if i != 0:
        res.append(i)
    return res


def get_arragment_array(max_arr):
    res = [1, 1, 2]
    for i in range(3, max_arr+1):
        res.append(sum(res[i] for i in range(i-3, i)))
    return res


def res_b(ones_subs, arragment_aray):
    res = 1
    for sub_len in ones_subs:
        res *= arragment_aray[sub_len]
    return res


def main():
    adapters = read_input()
    adapters.append(0)
    adapters.append(max(adapters) + 3)
    adapters = sorted(adapters)

    diffs = create_diffs(adapters)
    logger.info(f"Res {diffs}, res {diffs.count(1) * diffs.count(3)}")
    diffs.insert(0, 3)
    ones_subs = find_ones(diffs)
    logger.info(f"Ones subs {ones_subs}")
    aranngments_array = get_arragment_array(max(ones_subs))
    logger.info(f"Arr array {aranngments_array}")
    logger.info(f"Res b {res_b(ones_subs, aranngments_array)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
