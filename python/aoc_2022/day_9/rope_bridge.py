import numpy
from aoc_2022.utils import utils


def parse_series_of_motions(lines):
    series_of_motions = []
    for line in lines:
        direction, steps = line.split()[0], int(line.split()[1])

        series_of_motions.append((direction, steps))

    return series_of_motions


def determine_size_of_playground(series_of_motions):
    row_index = 0
    col_index = 0
    rows = 0
    cols = 0

    # assume 0,0 is bottom left
    for direction, steps in series_of_motions:

        if direction == "L":
            col_index -= steps
        if direction == "R":
            col_index += steps

        if direction == "U":
            row_index += steps
        if direction == "D":
            row_index -= steps

        print(row_index, col_index)

        if row_index > rows:
            rows = row_index
        if col_index > cols:
            cols = col_index

    return rows + 1, cols + 1


def point_touches_other_point(point, other_point):
    #  NW N NE
    #   W X  E
    #  SW S SE
    x1, y1 = point
    x2, y2 = other_point

    # horizonal and vertical distance is less or equal then 1
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

    # special case, same position
    if x1 == x2 and y1 == y2:
        return True

    # Left or Right
    if y1 == y2 and abs(x2 - x1) == 1:
        return True

    # Up or Down
    if x1 == x2 and abs(y2 - y1) == 1:
        return True

    # NE, SE, SW, NW
    if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
        return True

    return False


# def get_relative_position():
#  NW   N NE
#   W   X   E   1E
#  SW   S   SE  S1E
# 1SW  1S   1SE


# def move_tail(head_position, tail_position):
#     head_x, head_y = head_position
#     tail_x, tail_y = tail_position

#     # Move Right
#     if head_y == tail_y and (head_x - tail_x) == 1:
#         return move(tail_position, "R")
#     # Move Left
#     if head_y == tail_y and (head_x - tail_x) == -1:
#         return move(tail_position, "L")
#     # Move Up
#     if head_x == tail_x and (head_y - tail_y) == 1:
#         return move(tail_position, "U")
#     # Move Down
#     if head_x == tail_x and (head_y - tail_y) == -1:
#         return move(tail_position, "D")

#     raise RuntimeError("")


def calculate_tail_movement(head, tail) -> tuple[str, int]:
    x1, y1 = head
    x2, y2 = tail

    horizontal = x2 - x1
    vertical = y2 - y1

    breakpoint()

    if abs(horizontal) <= 1 and abs(vertical) <= 1:
        return "-"

    if horizontal == 2 and abs(vertical) <= 1:
        return "W"

    if horizontal == -2 and abs(vertical) <= 1:
        return "E"

    if abs(horizontal) <= 1 and vertical == -2:
        return "N"

    if abs(horizontal) <= 1 and vertical == 2:
        return "S"

    if horizontal == 2 and vertical == 2:
        return "SW"

    if horizontal == 2 and vertical == -2:
        return "NW"

    if horizontal == -2 and vertical == -2:
        return "NE"

    if horizontal == -2 and vertical == 2:
        return "SE"


def calculate_tail_movement2(head, tail):

    x1, y1 = head
    x2, y2 = tail

    delta_x = x2 - x1
    delta_y = y2 - y1

    # center is 2, 2
    direction_table = numpy.array(
        [
            [None, "SE", "S", "SW", None],
            ["SE", "0", "0", "0", "SW"],
            ["E", "0", "0", "0", "W"],
            ["NE", "0", "0", "0", "NW"],
            [None, "NE", "N", "NW", None],
        ]
    )

    x, y = 2 + delta_x, 2 + delta_y

    direction = direction_table[::-1][y, x]

    return direction


def move2(position, direction):
    movement_table = {
        "0": (0, 0),
        "N": (0, 1),
        "NE": (1, 1),
        "E": (1, 0),
        "SE": (1, -1),
        "S": (0, -1),
        "SW": (-1, -1),
        "W": (-1, 0),
        "NW": (-1, 1),
    }
    movement = movement_table[direction]

    return position[0] + movement[0], position[1] + movement[1]


def convert_to_cardinal_direction(direction):
    return {
        "U": "N",
        "R": "E",
        "D": "S",
        "L": "W",
    }[direction]


def move(position, direction):
    steps = 1
    x, y = position

    if direction == "-":
        return x, y

    if direction in ["L", "W"]:
        x -= steps

    if direction in ["R", "E"]:
        x += steps

    if direction in ["U", "N"]:
        y += steps

    if direction in ["D", "S"]:
        y -= steps

    if direction == "NE":
        y += steps
        x += steps

    if direction == "SE":
        y -= steps
        x += steps

    if direction == "SW":
        y -= steps
        x -= steps

    if direction == "NW":
        y += steps
        x -= steps

    return x, y


def solve_part_one(lines):
    series_of_motions = parse_series_of_motions(lines)
    # rows, cols = determine_size_of_playground(series_of_motions)

    head_position = 0, 0
    tail_position = 0, 0
    visited_points_tail = {tail_position}

    counter = 0

    for direction, steps in series_of_motions:
        direction = convert_to_cardinal_direction(direction)
        print(f"== {direction} {steps} ==")
        for _ in range(steps):
            new_head_position = move2(head_position, direction)
            print(
                f"moved head from {head_position} to {new_head_position} with move {direction} ({counter})"
            )
            head_position = new_head_position

            tail_direction = calculate_tail_movement2(head_position, tail_position)
            # if movement_tail[0] == "-":
            #     breakpoint()

            # for tail_direction in tail_directions:
            new_tail_position = move2(tail_position, tail_direction)
            print(
                f"moved tail from {tail_position} to {new_tail_position} with move {tail_direction}"
            )
            tail_position = new_tail_position
            visited_points_tail.add(tail_position)
            counter += 1

    print(visited_points_tail)
    print(len(visited_points_tail))


def solve_part_two(lines):
    pass


def main():

    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 9: Rope Bridge ---")
    answer_part_one = solve_part_one(lines)
    # print(f"Total score: {total_score_part_one}")

    print("--- Part Two ---")
    answer_part_two = solve_part_two(lines)
    # print(f"Total score: {total_score_part_two}")


if __name__ == "__main__":
    main()
