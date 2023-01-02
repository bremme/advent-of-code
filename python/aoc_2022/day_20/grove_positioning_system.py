from dataclasses import dataclass
from typing import Optional


@dataclass
class Number:
    value: int
    id: int
    left: Optional["Number"] = None
    right: Optional["Number"] = None


def parse(lines: list[str]):

    nodes: list[Number] = []

    for id_, line in enumerate(lines):
        node = Number(value=int(line), id=id_)

        nodes.append(node)

    num_nodes = len(nodes)

    # link nodes
    for i, node in enumerate(nodes):
        node.right = nodes[(i + 1) % num_nodes]
        node.left = nodes[(i - 1) % num_nodes]

    return nodes


def insert_node_to_the_right(left_node, node):

    right_node = left_node.right

    left_node.right = node
    node.left = left_node

    right_node.left = node
    node.right = right_node


def unlink_node(node):
    left_node = node.left
    right_node = node.right

    left_node.right = right_node
    right_node.left = left_node


def move_node(node, places, num_nodes):

    if places == 0:
        return

    insert_after_node = node

    # move to the right
    if places > 0:

        for _ in range(places % (num_nodes - 1)):
            insert_after_node = insert_after_node.right

    # move to the left
    else:
        # we move one extra position to be able to still insert the node to the right
        for _ in range((abs(places) % (num_nodes - 1)) + 1):
            insert_after_node = insert_after_node.left

    # do nothing if the found node is equal to our initial node
    if insert_after_node == node:
        return

    # remove node
    unlink_node(node)
    # connect node to the right of insert_after_node
    insert_node_to_the_right(insert_after_node, node)


def print_values(node, num_nodes):
    current_node = node
    start_node = node
    numbers = []
    counter = 0
    while True:
        numbers.append(current_node.value)
        current_node = current_node.right
        if current_node == start_node:
            break
        if counter == num_nodes:
            raise RuntimeError("Too many iterations")
        counter += 1
    print(numbers)


def get_value_at_relative_position(node, places, num_nodes):
    move = places % num_nodes

    current_node = node
    for _ in range(move):
        current_node = current_node.right

    return current_node.value


def solve_part_one(lines: list[str], example: bool) -> int:
    nodes = parse(lines)
    num_nodes = len(nodes)

    zero_node = None

    for i, node in enumerate(nodes):

        move_node(node, node.value, num_nodes)

        if node.value == 0:
            zero_node = node

    answers = []

    for relative_position in [1000, 2000, 3000]:
        answers.append(
            get_value_at_relative_position(zero_node, relative_position, num_nodes)
        )

    # 4, -3, 2 (example)
    # 6439 853 7596
    return sum(answers)


def solve_part_two(lines: list[str], example: bool) -> int:
    descryption_key = 811589153

    nodes = parse(lines)
    num_nodes = len(nodes)
    zero_node = None

    # apply decryption key
    for i, node in enumerate(nodes):
        node.value *= descryption_key

        if node.value == 0:
            zero_node = node

    # play rounds
    for round in range(1, 10 + 1):
        for i, node in enumerate(nodes):
            move_node(node, node.value, num_nodes)

    answers = []

    for relative_position in [1000, 2000, 3000]:
        answers.append(
            get_value_at_relative_position(zero_node, relative_position, num_nodes)
        )

    # 4, -3, 2 (example)
    # 6187555702472 3134357308886 -5561820465509
    return sum(answers)
