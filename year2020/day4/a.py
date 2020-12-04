import logging
import os
import re
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        data = f.read()
    passports_str = data.split("\n\n")
    passports = []
    for passport_str in passports_str:
        key_values = re.split("\n| ", passport_str.strip())
        passport = dict([key_value.split(":") for key_value in key_values])
        passports.append(passport)
    return passports


def is_valid_a(passport):
    required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    return all(req in passport for req in required)


def valid_year(year_str, min_v, max_v):
    return len(year_str) == 4 and min_v <= int(year_str) <= max_v


def valid_hgt(hgt):
    if len(hgt) < 3:
        return False
    unit = hgt[-2:]
    h_n = int(hgt[:-2])
    return (unit == "cm" and 150 <= h_n <= 193) or (unit == "in" and 59 <= h_n <= 76)


def valid_color(color):
    if len(color) != 7:
        return False
    valid_hex = {str(i) for i in range(10)}
    valid_hex = valid_hex | {"a", "b", "c", "d", "e", "f"}
    return color[0] == "#" and all(c in valid_hex for c in color[1:])


def valid_eye_color(color):
    valid_colors = "amb blu brn gry grn hzl oth".split(" ")
    return color in valid_colors


def valid_pid(pid):
    int(pid)
    return len(pid) == 9


def is_valid_b(passport):
    if not is_valid_a(passport):
        return False

    try:
        is_valid = (
            is_valid_a(passport)
            and valid_year(passport["byr"], 1920, 2002)
            and valid_year(passport["iyr"], 2010, 2020)
            and valid_year(passport["eyr"], 2020, 2030)
            and valid_hgt(passport["hgt"])
            and valid_color(passport["hcl"])
            and valid_eye_color(passport["ecl"])
            and valid_pid(passport["pid"])
        )
    except Exception:
        logger.exception("Validation failed")
        return False
    return is_valid


def main():
    passports = parse_input()
    # logger.info(f"Passports {passports}")
    valid_passports = [is_valid_a(passport) for passport in passports]
    # "cid"
    logger.info(f"Valid passports A {sum(valid_passports)}")
    valid_passports = [is_valid_b(passport) for passport in passports]
    logger.info(f"Valid passports B {sum(valid_passports)}")


if __name__ == "__main__":
    init_logging()
    main()
