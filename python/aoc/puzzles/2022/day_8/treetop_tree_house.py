import logging

import numpy

logger = logging.getLogger()


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
            logger.debug(f"{element}  ", end="")
        logger.debug("")
    logger.debug("")


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

    for row_index, row in enumerate(forest_tree_height_view):

        highest_tree_in_row = 0

        for col_index, tree_height in enumerate(row):

            # check if tree is at the edge
            if col_index == 0:
                highest_tree_in_row = tree_height
                forest_tree_visible_view[row_index][col_index] = "Y"
                continue

            # check if tree is higher then previous trees
            if tree_height > highest_tree_in_row:
                forest_tree_visible_view[row_index, col_index] = "Y"
                highest_tree_in_row = tree_height

    return forest_tree_visible


def get_number_of_visible_trees(forest, row_index, col_index, direction):

    num_rows = len(forest)
    num_cols = len(forest[0])

    def update_index(row_index, col_index):
        if direction == "up":
            row_index -= 1

        if direction == "left":
            col_index -= 1

        if direction == "right":
            col_index += 1

        if direction == "down":
            row_index += 1

        return row_index, col_index

    if is_edge(row_index, col_index, num_rows, num_cols):
        return 0

    treehouse_height = forest[row_index, col_index]
    num_visible_trees = 0
    highest_tree_in_direction = 0

    while True:

        # update index
        row_index, col_index = update_index(row_index, col_index)

        tree_height = forest[row_index, col_index]

        # if tree_height >= highest_tree_in_direction:
        num_visible_trees += 1

        # set new highest tree in this direction
        # if tree_height > highest_tree_in_direction:
        #     highest_tree_in_direction = tree_height

        # if this tree is equal or higher we can't see anymore trees
        if tree_height >= treehouse_height:
            break

        if is_edge(row_index, col_index, num_rows, num_cols):
            break

    return num_visible_trees


def calculate_scenic_score(forest, row_index, col_index):
    # how many visible trees up
    num_visible_trees_up = get_number_of_visible_trees(
        forest, row_index, col_index, "up"
    )
    # how many visible trees left
    num_visible_trees_left = get_number_of_visible_trees(
        forest, row_index, col_index, "left"
    )
    # how many visible trees down
    num_visible_trees_down = get_number_of_visible_trees(
        forest, row_index, col_index, "down"
    )
    # how many visible trees right
    num_visible_trees_right = get_number_of_visible_trees(
        forest, row_index, col_index, "right"
    )

    # logger.debug("up", num_visible_trees_up)
    # logger.debug("left", num_visible_trees_left)
    # logger.debug("down", num_visible_trees_down)
    # logger.debug("right", num_visible_trees_right)

    return (
        num_visible_trees_up
        * num_visible_trees_left
        * num_visible_trees_right
        * num_visible_trees_down
    )


def solve_part_one(lines: list[str], example: bool) -> int:
    forest_tree_height = parse_forest_tree_height(lines)
    forest_tree_visible = build_forest_tree_visible(forest_tree_height)

    print_forest(forest_tree_height)
    print_forest(forest_tree_visible)

    logger.debug("Look from left")
    forest_tree_visible = look_from_side(
        forest_tree_height, forest_tree_visible, "left"
    )
    logger.debug("After look from left")
    print_forest(forest_tree_visible)

    logger.debug("Look from top")
    forest_tree_visible = look_from_side(forest_tree_height, forest_tree_visible, "top")
    logger.debug("After look from top")
    print_forest(forest_tree_visible)

    logger.debug("Look from right")
    forest_tree_visible = look_from_side(
        forest_tree_height, forest_tree_visible, "right"
    )
    logger.debug("After look from right")
    print_forest(forest_tree_visible)

    logger.debug("Look from bottom")
    forest_tree_visible = look_from_side(
        forest_tree_height, forest_tree_visible, "bottom"
    )
    logger.debug("After look from bottom")
    print_forest(forest_tree_visible)

    return numpy.count_nonzero(forest_tree_visible == "Y")


def solve_part_two(lines: list[str], example: bool) -> int:
    # find tree with highest scenic score
    forest = parse_forest_tree_height(lines)
    scenic_scores = numpy.zeros(forest.shape)

    # example puzzle input
    logger.debug(calculate_scenic_score(forest, 1, 2))  # 4
    logger.debug(calculate_scenic_score(forest, 3, 2))  # 8

    for row_index, row in enumerate(forest):
        for col_index, _ in enumerate(row):
            scenic_scores[row_index, col_index] = calculate_scenic_score(
                forest, row_index, col_index
            )

    logger.debug(scenic_scores)

    return scenic_scores.max()
