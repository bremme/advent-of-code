import sys
from pathlib import Path

import numpy


def parse_forest_tree_height(lines):
    forest = []
    for line in lines:
        row = []
        for char in line:
            tree = int(char)
            row.append(tree)
        forest.append(row)

    return numpy.array(forest)


def build_forest_tree_visible(forest: list[list[int]]):
    rows, cols = len(forest), len(forest[0])
    forest = []

    for _ in range(rows):
        forest.append(["N" for _ in range(cols)])

    return numpy.array(forest)


def print_forest(forest):
    for row in forest:
        for element in row:
            print(f"{element}  ", end="")
        print()
    print()


def is_edge(row_index, col_index, num_rows, num_cols):
    if (
        row_index == 0
        or col_index == 0
        or row_index == num_rows - 1
        or col_index == num_cols - 1
    ):
        return True

    return False


def look_from_side(forest_tree_height, forest_tree_visible, side):

    if side == "left":
        forest_tree_height_view = forest_tree_height
        forest_tree_visible_view = forest_tree_visible
    # rotate left 90 deg
    if side == "top":
        forest_tree_height_view = numpy.rot90(forest_tree_height, k=1)
        forest_tree_visible_view = numpy.rot90(forest_tree_visible, k=1)
    # rotate left/right 180 deg
    if side == "right":
        forest_tree_height_view = numpy.rot90(forest_tree_height, k=2)
        forest_tree_visible_view = numpy.rot90(forest_tree_visible, k=2)
    # rotate left 270 deg
    if side == "bottom":
        forest_tree_height_view = numpy.rot90(forest_tree_height, k=3)
        forest_tree_visible_view = numpy.rot90(forest_tree_visible, k=3)

    num_rows = len(forest_tree_height_view)
    num_cols = len(forest_tree_visible_view[0])

    for row_index, row in enumerate(forest_tree_height_view):

        highest_tree_in_row = 0

        for col_index, tree_height in enumerate(row):

            # check if tree is around the edge
            if col_index == 0:
                highest_tree_in_row = tree_height
                # if tree_height == 0:
                #     continue
                forest_tree_visible_view[row_index][col_index] = "Y"
                continue

            # check if tree is higher then previous trees
            if tree_height > highest_tree_in_row:
                forest_tree_visible_view[row_index, col_index] = "Y"
                highest_tree_in_row = tree_height

    return forest_tree_visible


def part_one(lines):
    forest_tree_height = parse_forest_tree_height(lines)
    forest_tree_visible = build_forest_tree_visible(forest_tree_height)

    print_forest(forest_tree_height)
    print_forest(forest_tree_visible)

    print("Look from left")
    forest_tree_visible = look_from_side(
        forest_tree_height, forest_tree_visible, "left"
    )
    print("After look from left")
    print_forest(forest_tree_visible)

    print("Look from top")
    forest_tree_visible = look_from_side(forest_tree_height, forest_tree_visible, "top")
    print("After look from top")
    print_forest(forest_tree_visible)

    print("Look from right")
    forest_tree_visible = look_from_side(
        forest_tree_height, forest_tree_visible, "right"
    )
    print("After look from right")
    print_forest(forest_tree_visible)

    print("Look from bottom")
    forest_tree_visible = look_from_side(
        forest_tree_height, forest_tree_visible, "bottom"
    )
    print("After look from bottom")
    print_forest(forest_tree_visible)

    print(numpy.count_nonzero(forest_tree_visible == "Y"))

    # 1501 too low
    # 1602 too low


def part_two(lines):
    pass


def main(input_file):
    input_file_path = Path(input_file)

    with open(input_file_path, "r") as fh:
        lines = [line for line in fh.read().splitlines()]

    part_one(lines)
    part_two(lines)


if __name__ == "__main__":
    input_file = sys.argv[1]

    main(input_file)
