from collections import namedtuple
import logging
import os
import math

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

Ingredient = namedtuple('Ingredient', ['label', 'quant'])


class Node:
    def __init__(self, ingredients, result):
        super().__init__()
        self.ingredients = ingredients
        self.result = result
        self.required = 0
        self.visited = False

    def __repr__(self):
        return '%s->%s' % (self.ingredients, self.result)


def read_input():
    def create_ingredient(ing_str):
        quant, label = ing_str.strip().split(' ')
        return Ingredient(label, int(quant))

    graph = {}
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        for line in f:
            line = line.strip()
            ingredients_str, result_str = line.split(' => ')
            ingredients = [create_ingredient(ing_str) for ing_str in ingredients_str.split(',')]
            result = create_ingredient(result_str)
            graph[result.label] = Node(ingredients, result)
    graph['ORE'] = Node([], Ingredient('ORE', 1))
    return graph


def topological_sort(graph, node: Node, res=None):
    if res is None:
        res = []
    node.visited = True
    for ing in node.ingredients:
        sub_node = graph[ing.label]
        if not sub_node.visited:
            topological_sort(graph, sub_node, res)
    res.append(node)
    return res


def calculate_required(graph, nodes, initial_required):
    reset_required(nodes)
    for node in nodes:
        if node.result.label == 'FUEL':
            node.required = initial_required
        reaction_times_used = math.ceil(node.required/node.result.quant)
        node.required = reaction_times_used * node.result.quant
        for ing in node.ingredients:
            sub_node = graph[ing.label]
            sub_node.required += reaction_times_used * ing.quant


def reset_required(nodes):
    for node in nodes:
        node.required = 0


MAX_ORE = 1000000000000


def binary_search_max(graph, nodes, left=1, right=None):
    to_check = None
    if left + 1 == right:
        return left

    if right is None:
        to_check = left * 2
    else:
        to_check = (left + right + 1) // 2
    # logger.info('[%s, %s], check %s', left, right, to_check)
    calculate_required(graph, nodes, initial_required=to_check)
    if graph['ORE'].required <= MAX_ORE:
        return binary_search_max(graph, nodes, left=to_check, right=right)
    else:
        return binary_search_max(graph, nodes, left=left, right=to_check)


def main():
    graph = read_input()
    sorted_nodes = topological_sort(graph, graph['FUEL'])
    sorted_nodes.reverse()
    calculate_required(graph, sorted_nodes, initial_required=1)
    res = graph['ORE'].required
    logger.info('Result part a: %s', res)
    res = binary_search_max(graph, sorted_nodes)
    logger.info('Result part b: %s.', res)


if __name__ == "__main__":
    init_logging()
    main()
