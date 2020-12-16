import logging
import time
import os
import math
from typing import List, Set, Dict

from collections import namedtuple
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

Ticket = namedtuple("Ticket", ["fields"])
Rule = namedtuple("Rule", ["name", "ranges"])
TaskInput = namedtuple("TaskInput", ["rules", "my_ticket", "tickets"])

INPUT_FILE = "input.txt"


def parse_ticket(line):
    line = line.strip()
    return Ticket([int(x) for x in line.split(",")])


def parse_rule(line):
    field_name, ranges_str = line.split(": ")
    ranges = [
        tuple(int(x) for x in range_str.split("-"))
        for range_str in ranges_str.split(" or ")
    ]
    return Rule(field_name, ranges)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        content = f.read().strip()
        rules_str, my_ticket_str, tickets_str = content.split("\n\n")
        rules = [parse_rule(rule_str) for rule_str in rules_str.split("\n")]
        my_ticket = parse_ticket(my_ticket_str.split("\n")[1])
        tickets = [
            parse_ticket(ticket_str) for ticket_str in tickets_str.split("\n")[1:]
        ]
        return TaskInput(rules, my_ticket, tickets)


def check_rules(number: int, rules: List[Rule]) -> bool:
    for rule in rules:
        for range_ in rule.ranges:
            if range_[0] <= number <= range_[1]:
                return True
    return False


def get_invalid_fields(rules: List[Rule], tickets: List[Ticket]) -> List[int]:
    for ticket in tickets:
        for number in ticket.fields:
            if not check_rules(number, rules):
                yield number


def is_valid_ticket(rules: List[Rule], ticket: Ticket) -> bool:
    return all(check_rules(number, rules) for number in ticket.fields)


def is_valid_rule(numbers: List[int], rule: Rule) -> bool:
    return all(check_rules(number, [rule]) for number in numbers)


def get_matching_fields(input: TaskInput):
    tickets = input.tickets + [input.my_ticket]
    res = []
    for i in range(len(tickets[0].fields)):
        numbers = [ticket.fields[i] for ticket in tickets]
        res.append({rule.name for rule in input.rules if is_valid_rule(numbers, rule)})
    return res


def get_field_order(matching_fields: List[Set[str]]) -> List[str]:
    used_fields = set()
    sorted_matching_fields = sorted(enumerate(matching_fields), key=lambda x: len(x[1]))
    res = {}
    for idx, fields in sorted_matching_fields:
        assert len(fields - used_fields) == 1
        field = (fields - used_fields).pop()
        used_fields.add(field)
        res[field] = idx
    return res


def get_res_b(ticket: Ticket, field_order: Dict[str, int]) -> int:
    departue_fields = [
        idx for name, idx in field_order.items() if name.startswith("departure")
    ]
    ticket_values = [ticket.fields[idx] for idx in departue_fields]
    return math.prod(ticket_values)


def main():
    input = read_input()
    invalid_fields = list(get_invalid_fields(input.rules, input.tickets))
    logger.info(f"Res A {sum(invalid_fields)}")
    input = input._replace(
        tickets=[
            ticket for ticket in input.tickets if is_valid_ticket(input.rules, ticket)
        ]
    )
    matching_fields = get_matching_fields(input)
    field_order = get_field_order(matching_fields)
    logger.info(f"Field order {field_order}")
    logger.info(f"Res B {get_res_b(input.my_ticket, field_order)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
