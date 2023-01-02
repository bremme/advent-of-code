from dataclasses import dataclass
from multiprocessing import current_process
from turtle import st
from typing import Optional


@dataclass
class Number:
    value: int
    id: int
    left: Optional["Number"] = None
    right: Optional["Number"] = None


def parse(lines: list[str]):

    previous_node = None
    # first_node = None
    nodes: list[Number] = []

    for i, line in enumerate(lines):
        node = Number(value=int(line), id=i, left=previous_node)
        nodes.append(node)

        if i == 0:
            first_node = node
            previous_node = node
            continue

        previous_node.right = node

        previous_node = node

        if i == len(lines) - 1:
            first_node.left = node
            node.right = first_node

    return nodes


def get_linked_node(node, places, direction, num_nodes):
    linked_node = node

    for _ in range(abs(places)):
        linked_node = getattr(linked_node, direction)

    return linked_node


def get_linked_node2(node, places, direction, num_nodes):
    linked_node = node

    extra = -1 if direction == "left" else 1
    extra *= abs(places) // num_nodes

    # print(direction, extra, places // num_nodes)
    # print(abs(places) // num_nodes)

    for _ in range(abs(places + extra) % num_nodes):
        linked_node = getattr(linked_node, direction)

    return linked_node


def move_node2(node, places, num_nodes):

    if places == 0:
        return

    direction = "right" if places > 0 else "left"

    # remove node
    left_node = node.left
    right_node = node.right

    left_node.right = right_node
    right_node.left = left_node

    # insert_at_node = get_linked_node(node, places, direction, num_nodes)
    # extra = -1 if direction == "left" else 1
    # extra *= abs(places) // num_nodes
    # print(extra)

    insert_at_node = get_linked_node2(node, places, direction, num_nodes)

    # print(direction, abs(places) // num_nodes, places // num_nodes)

    # if insert_at_node != get_linked_node(node, places, direction, num_nodes):
    #     breakpoint()

    # insert node
    if direction == "right":
        # print("right")
        left_node = insert_at_node
        right_node = insert_at_node.right

        left_node.right = node
        node.left = left_node

        right_node.left = node
        node.right = right_node

    if direction == "left":
        # print("left")
        right_node = insert_at_node
        left_node = insert_at_node.left

        right_node.left = node
        node.right = right_node

        left_node.right = node
        node.left = left_node


def insert_node_to_the_right(insert_after_node, node):
    left_node = insert_after_node
    right_node = insert_after_node.right

    left_node.right = node
    node.left = left_node

    right_node.left = node
    node.right = right_node


def insert_node_to_the_left(insert_before_node, node):
    right_node = insert_before_node
    left_node = insert_before_node.left

    right_node.left = node
    node.right = right_node

    left_node.right = node
    node.left = left_node


def unlink_node(node):
    left_node = node.left
    right_node = node.right

    left_node.right = right_node
    right_node.left = left_node


def move_node(node, places, num_nodes):

    if places == 0:
        return

    # remove node
    unlink_node(node)

    extra = 1 if places > 0 else -1
    extra *= 1 if (abs(places) // num_nodes) else 0

    # move to the right
    if places > 0:

        insert_after_node = node

        for _ in range((places + extra) % num_nodes):
            insert_after_node = insert_after_node.right

        # connect node to the right of insert_after_node
        insert_node_to_the_right(insert_after_node, node)

        return

    # move to the left
    insert_before_node = node

    for _ in range(abs(places + extra) % num_nodes):
        insert_before_node = insert_before_node.left

    # connect node to the left of insert_before_node
    insert_node_to_the_left(insert_before_node, node)


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
        # print_values(node)
        move_node(node, node.value, num_nodes)
        # if i == (num_nodes - 1):
        #     print_values(node)
        if node.value == 0:
            zero_node = node

    # print_values(node)

    v1 = get_value_at_relative_position(zero_node, 1000, num_nodes)
    v2 = get_value_at_relative_position(zero_node, 2000, num_nodes)
    v3 = get_value_at_relative_position(zero_node, 3000, num_nodes)

    print(v1, v2, v3)
    # example 4, -3, 2
    # 6439 853 7596
    return v1 + v2 + v3


def solve_part_two(lines: list[str], example: bool) -> int:
    descryption_key = 811589153

    nodes = parse(lines)
    num_nodes = len(nodes)
    zero_node = None

    # apply decryption key
    for i, node in enumerate(nodes):
        print(f"apply descyption key for node {i}")
        node.value *= descryption_key

        if node.value == 0:
            zero_node = node

    # play rounds
    for round in range(1, 10 + 1):

        for i, node in enumerate(nodes):
            print_values(node, num_nodes)
            move_node(node, node.value, num_nodes)
            if i == (num_nodes - 1):
                print_values(node, num_nodes)

        print(f"After {round} rounds of mixing:")

        # breakpoint()
        # print_values(nodes[0])
    v1 = get_value_at_relative_position(zero_node, 1000, len(nodes))
    v2 = get_value_at_relative_position(zero_node, 2000, len(nodes))
    v3 = get_value_at_relative_position(zero_node, 3000, len(nodes))

    print(v1, v2, v3)
    # 4, -3, 2
    return v1 + v2 + v3
