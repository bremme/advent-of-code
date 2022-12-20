from enum import Enum, auto

import numpy
from aoc_2022.utils import utils


class Direction(Enum):
    NONE = "0"
    NORTH = "N"
    NORTH_EAST = "NE"
    EAST = "E"
    SOUTH_EAST = "SE"
    SOUTH = "S"
    SOUTH_WEST = "SW"
    WEST = "W"
    NORTH_WEST = "NW"


# class Movement(Enum):
#     Direction.NONE = (0, 0)
#     Direction.NORTH = (1, 0)
#     Direction.NORTH_EAST = (1, 1)
#     Direction.EAST = (0, 1)
#     Direction.SOUTH_EAST = (-1, 1)
#     Direction.SOUTH = (-1, 0)
#     Direction.SOUTH_WEST = (-1, -1)
#     Direction.WEST = (0, -1)
#     Direction.NORTH_WEST = (1, -1)


class Move:
    def __init__(self, num_rows, num_cols) -> None:
        self.num_rows = num_rows
        self.num_cols = num_cols

    @staticmethod
    def from_direction(direction: Direction):
        movement = Movement(direction)
        return Move(movement.value[0], movement.value[1])


class Motion:
    def __init__(self, direction, steps) -> None:
        self.direction = direction
        self.steps = steps


class Point:
    def __init__(self, row=0, col=0) -> None:
        self.row = row
        self.col = col

    def move(self, move: Move):
        self.row += move.num_rows
        self.col += move.num_cols


class Knot(Point):
    def __init__(self, row, col, symbol) -> None:
        super().__init__(row, col)
        self.head = None
        self.symbol = symbol

    def follow(self, head):
        delta_row = self.row - head.row
        delta_col = self.col - head.col

        # center is 2, 2
        DIRECTION_TABLE = numpy.array(
            [
                ["0", "SE", "S", "SW", "0"],
                ["SE", "0", "0", "0", "SW"],
                ["E", "0", "0", "0", "W"],
                ["NE", "0", "0", "0", "NW"],
                ["0", "NE", "N", "NW", "0"],
            ]
        )

        row, col = 2 + delta_row, 2 + delta_col


class Robe:
    def __init__(self, start: Point, number_of_knots) -> None:
        self.number_of_knots = number_of_knots
        self.knots = []

        head = None

        for i in range(number_of_knots):
            if i == 0:
                symbol = "H"
            else:
                symbol = str(i)

            knot = Knot(start.row, start.col, symbol)

            self.knots.append(knot)

    @property
    def head(self):
        return self.knots[0]

    @property
    def tail(self):
        return self.knots[-1]

    def move_head(self, motion: Motion):
        for _ in range(motion.steps):
            move = Move.from_direction(motion.direction)
            self.head.move(motion.direction)

            for head, knot in zip(self.knots[:-1], self.knots[1:]):
                knot.follow(head)


class PlayGround:
    def __init__(self, series_of_motions: list[Motion], robe: Robe) -> None:
        self._determine_playground(series_of_motions)
        self.series_of_motions = series_of_motions
        self.robe = robe

    def _determine_playground(self, series_of_motions):
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

        self.num_rows = row_max - row_min + 1
        self.num_cols = col_max - col_min + 1

        self.start = Point(row=abs(row_min), col=abs(col_min))

    def play(self):
        for motion in self.series_of_motions:
            print(f"== {motion.direction.value} {motion.steps} ==")
            self.robe.move_head(motion)


def convert_to_cardinal_direction(direction):
    return {
        "U": Direction.NORTH,
        "R": Direction.EAST,
        "D": Direction.SOUTH,
        "L": Direction.WEST,
    }[direction]


def parse_series_of_motions(lines) -> list[Motion]:
    series_of_motions = []
    for line in lines:
        direction = convert_to_cardinal_direction(line.split()[0])
        steps = int(line.split()[1])

        series_of_motions.append(Motion(direction, steps))

    return series_of_motions


def solve_part_one(lines, example=False):
    robe = Robe(number_of_knots=1)

    series_of_motions = parse_series_of_motions(lines)

    playground = PlayGround(series_of_motions=series_of_motions, robe=robe)

    playground.play()


def main():

    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 9: Rope Bridge ---")
    answer_part_one = solve_part_one(lines)
    print(f"Answer part one: {answer_part_one}")

    # print("--- Part Two ---")
    # answer_part_two = solve_part_two(lines)
    # print(f"Answer part two: {answer_part_two}")


if __name__ == "__main__":
    main()
