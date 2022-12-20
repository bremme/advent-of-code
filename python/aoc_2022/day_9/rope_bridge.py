import numpy
from aoc_2022.utils import utils


class Point:
    MOVEMENT_TABLE = {
        # direction : (row, col)
        "0": (0, 0),
        "N": (1, 0),
        "NE": (1, 1),
        "E": (0, 1),
        "SE": (-1, 1),
        "S": (-1, 0),
        "SW": (-1, -1),
        "W": (0, -1),
        "NW": (1, -1),
    }

    def __init__(self, row=0, col=0) -> None:
        self.row = row
        self.col = col

    @property
    def position(self):
        return self.row, self.col

    def move(self, direction):
        movement = self.MOVEMENT_TABLE[direction]
        self.row += movement[0]
        self.col += movement[1]


class PlayGround:
    def __init__(self) -> None:
        pass


def parse_series_of_motions(lines):
    series_of_motions = []
    for line in lines:
        direction = convert_to_cardinal_direction(line.split()[0])
        steps = int(line.split()[1])

        series_of_motions.append((direction, steps))

    return series_of_motions


def determine_playground(series_of_motions):
    x, y = 0, 0

    x_coordinates = [x]
    y_coordinates = [y]

    # Use Cartesian coordinates
    for direction, steps in series_of_motions:

        for _ in range(steps):
            x, y = move((x, y), direction)
            x_coordinates.append(x)
            y_coordinates.append(y)

    x_min, x_max = min(x_coordinates), max(x_coordinates)
    y_min, y_max = min(y_coordinates), max(y_coordinates)

    size_x = x_max - x_min + 1
    size_y = y_max - y_min + 1

    start = abs(x_min), abs(y_min)

    return start, (size_x, size_y)


def determine_playground_2(series_of_motions):
    position = Point()

    visited_rows = []
    visited_cols = []

    for direction, steps in series_of_motions:
        for _ in range(steps):
            position.move(direction)
            visited_rows.append(position.row)
            visited_cols.append(position.col)

    row_min, row_max = min(visited_rows), max(visited_rows)
    col_min, col_max = min(visited_cols), max(visited_cols)

    num_rows = row_max - row_min + 1
    num_cols = col_max - col_min + 1

    start = Point(row=abs(row_min), col=abs(col_min))

    return start, (num_rows, num_cols)


def calculate_tail_movement(head, tail):

    x1, y1 = head
    x2, y2 = tail

    delta_x = x2 - x1
    delta_y = y2 - y1

    # center is 2, 2
    DIRECTION_TABLE = numpy.array(
        [
            [None, "SE", "S", "SW", None],
            ["SE", "0", "0", "0", "SW"],
            ["E", "0", "0", "0", "W"],
            ["NE", "0", "0", "0", "NW"],
            [None, "NE", "N", "NW", None],
        ]
    )

    x, y = 2 + delta_x, 2 + delta_y

    direction = DIRECTION_TABLE[::-1][y, x]

    if direction is None:
        raise RuntimeError("Can't calculate tail movement, something is wrong")

    return direction


def move(position, direction):
    MOVEMENT_TABLE = {
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
    movement = MOVEMENT_TABLE[direction]
    new_position = position[0] + movement[0], position[1] + movement[1]

    return new_position


def convert_to_cardinal_direction(direction):
    return {
        "U": "N",
        "R": "E",
        "D": "S",
        "L": "W",
    }[direction]


class Knot(Point):
    def __init__(self, row=0, col=0) -> None:
        super().__init__(row, col)


class Robe:
    def __init__(self, start: Point, number_of_knots) -> None:
        self.knots: list[Point] = [
            Point(start.row, start.col) for _ in range(number_of_knots + 1)
        ]
        self.number_of_knots = number_of_knots

    @property
    def head(self):
        return self.knots[0]

    @property
    def tail(self):
        return self.knots[-1]

    def move_head(self, direction):
        self.head.move(direction)
        # move following knots


def solve_part_one_2(lines):
    series_of_motions = parse_series_of_motions(lines)
    start, size = determine_playground_2(series_of_motions)
    print(f"Head starts at {start} on playground with size {size}")

    robe = Robe(start, number_of_knots=1)
    # tail = Point(start.row, start.col)
    visited_points_tail = {robe.tail.position}

    counter = 0

    for direction, steps in series_of_motions:

        print(f"== {direction} {steps} ==")
        for _ in range(steps):
            # Move head (step-=by-step)
            robe.move_head(direction)

            # Move tail (single step )
            tail_direction = calculate_tail_movement(head_position, tail_position)
            new_tail_position = move(tail_position, tail_direction)
            print(
                f"moved tail from {tail_position} to {new_tail_position} with move {tail_direction}"
            )
            tail_position = new_tail_position

            # record unique visited tail positions
            visited_points_tail.add(tail_position)
            counter += 1

    return len(visited_points_tail)


def solve_part_one(lines):
    series_of_motions = parse_series_of_motions(lines)
    start, size = determine_playground(series_of_motions)
    print(f"Head starts at {start} on playground with size {size}")

    head_position = start
    tail_position = start
    visited_points_tail = {tail_position}

    counter = 0

    for direction, steps in series_of_motions:

        print(f"== {direction} {steps} ==")
        for _ in range(steps):
            # Move head (step-=by-step)
            new_head_position = move(head_position, direction)
            print(
                f"moved head from {head_position} to {new_head_position} with move {direction} ({counter})"
            )
            head_position = new_head_position

            # Move tail (single step )
            tail_direction = calculate_tail_movement(head_position, tail_position)
            new_tail_position = move(tail_position, tail_direction)
            print(
                f"moved tail from {tail_position} to {new_tail_position} with move {tail_direction}"
            )
            tail_position = new_tail_position

            # record unique visited tail positions
            visited_points_tail.add(tail_position)
            counter += 1

    return len(visited_points_tail)


def print_playground(size, knot_positions):
    lines = []
    size_x, size_y = size

    for y in range(size_y):
        for x in range(size_x):
            pass


def solve_part_two(lines):
    series_of_motions = parse_series_of_motions(lines)
    start, size = determine_playground(series_of_motions)
    print(f"Head starts at {start} on playground with size {size}")

    knot_positions = []
    for _ in range(10):
        knot_positions.append(start)

    visited_points_tail = {start}

    counter = 0

    for direction, steps in series_of_motions:
        print(f"== {direction} {steps} ==")
        for _ in range(steps):
            # Move head (step-=by-step)
            head_position = knot_positions[0]
            new_head_position = move(head_position, direction)
            print(
                f"\nmoved head from {head_position} to {new_head_position} with move {direction} ({counter})"
            )
            knot_positions[0] = new_head_position

            for knot_index, knot_tail_position in enumerate(
                knot_positions[1:], start=1
            ):
                # print(knot_index, knot_tail_position)
                # Move knot
                knot_head_position = knot_positions[knot_index - 1]

                knot_direction = calculate_tail_movement(
                    knot_head_position, knot_tail_position
                )
                new_knot_position = move(knot_tail_position, knot_direction)
                print(
                    f"moved knot {knot_index} from {knot_tail_position} to {new_knot_position} with move {knot_direction}"
                )
                knot_positions[knot_index] = new_knot_position

                # record unique visited tail positions
                if knot_index + 1 == len(knot_positions):
                    visited_points_tail.add(new_knot_position)

                # if knot_index == 2:
                #     breakpoint()

            counter += 1

    return len(visited_points_tail)


def main():

    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    # print("--- Day 9: Rope Bridge ---")
    # answer_part_one = solve_part_one(lines)
    # print(f"Answer part one: {answer_part_one}")

    print("--- Part Two ---")
    answer_part_two = solve_part_two(lines)
    print(f"Answer part two: {answer_part_two}")


if __name__ == "__main__":
    main()
