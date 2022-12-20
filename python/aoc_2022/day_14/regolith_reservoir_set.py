from collections import namedtuple
from dataclasses import dataclass
from enum import Enum


@dataclass
class Movement:
    delta_row: int
    delta_column: int


DOWN = Movement(1, 0)
DOWN_LEFT = Movement(1, -1)
DOWN_RIGHT = Movement(1, 1)


@dataclass(eq=True, frozen=True)
class Coordinate:
    row: int
    column: int

    def __add__(self, move: Movement):
        return Coordinate(
            row=self.row + move.delta_row, column=self.column + move.delta_column
        )

    def __sub__(self, move: Movement):
        return Coordinate(
            row=self.row - move.delta_row, column=self.column - move.delta_column
        )


# Coordinate = namedtuple("Coordinate", ["row", "column"])


# class Coordinate:
#     def __init__(self, row, column) -> None:
#         self.row = row
#         self.column = column
#         self.__hash

#     def __eq__(self, other):
#         if type(other) is type(self):
#             return (self.row, self.column) == (other.row, other.column)
#         else:
#             return False

#     def __hash__(self):
#         return hash((self.row, self.column))

#     def __repr__(self):
#         return f"Coordinate(row={self.row}, column={self.column})"


def line_coordinates(start: Coordinate, end: Coordinate):
    coordinates = []

    # horizontal line
    if start.row == end.row:
        # if line is right to left -> swap
        if start.column > end.column:
            start, end = end, start

        for column in range(start.column, end.column + 1):
            coordinates.append(Coordinate(row=start.row, column=column))

        return coordinates

    # vertical line
    if start.column == end.column:
        # if line is bottom to top -> swap
        if start.row > end.row:
            start, end = end, start

        for row in range(start.row, end.row + 1):
            coordinates.append(Coordinate(row=row, column=start.column))

        return coordinates

    raise ValueError("Start and end coordinates should be horizontal or vertical")


def parse(lines):

    rocks = set()

    for line in lines:
        numbers = [int(element) for element in line.replace(" -> ", ",").split(",")]
        for i in range(0, len(numbers) - 2, 2):
            start = Coordinate(row=numbers[i + 1], column=numbers[i])
            end = Coordinate(row=numbers[i + 3], column=numbers[i + 2])
            coordinates = line_coordinates(start, end)
            rocks.update(coordinates)

    return rocks


def get_possible_coordinates(start):
    # return [
    #     start + Move.DOWN.value,
    #     start + Move.DOWN_LEFT.value,
    #     start + Move.DOWN_RIGHT.value,
    # ]
    return [
        Coordinate(
            start.row + DOWN.delta_row,
            start.column + DOWN.delta_column,
        ),
        Coordinate(
            start.row + DOWN_LEFT.delta_row,
            start.column + DOWN_LEFT.delta_column,
        ),
        Coordinate(
            start.row + DOWN_RIGHT.delta_row,
            start.column + DOWN_RIGHT.delta_column,
        ),
    ]


class Map:
    def __init__(self, rocks: set, start) -> None:
        self.rocks = rocks
        self.sand = set()
        self.start = start
        self.calculate_size()

    def calculate_size(self):
        rows = [coordinate.row for coordinate in self.rocks]
        columns = [coordinate.column for coordinate in self.rocks]
        self.min_row, self.max_row = 0, max(rows)
        self.min_column, self.max_column = min(columns), max(columns)
        self.width = self.max_column - self.min_column + 1
        self.height = self.max_row - self.min_row + 1

    def draw_sand(self, coordinate):
        self.sand.add(coordinate)

    def is_air(self, coordinate):
        return coordinate not in self.rocks and coordinate not in self.sand

    def is_on_map(self, coordinate):
        if not (self.min_row <= coordinate.row <= self.max_row):
            return False

        if not (self.min_column <= coordinate.column <= self.max_column):
            return False

        return True

    def print(self, printer=print):
        rock_symbol = "🟫"
        air_symbol = "⬛"
        source_symbol = "🟦"
        sand_symbol = "🟨"

        for row in range(self.height):
            line = []
            for column in range(self.width):
                coordinate = Coordinate(
                    row=row + self.min_row, column=column + self.min_column
                )

                if coordinate in self.rocks:
                    line.append(rock_symbol)
                    continue

                if coordinate in self.sand:
                    line.append(sand_symbol)
                    continue

                if coordinate == self.start:
                    line.append(source_symbol)
                    continue

                line.append(air_symbol)
            printer("".join(line))


def pour_unit_of_sand_from_source(map: Map):
    coordinate = map.start

    while coordinate.row <= map.max_row:
        for new_coordinate in get_possible_coordinates(coordinate):
            if map.is_air(new_coordinate):
                coordinate = new_coordinate
                break

        # not moved (no break) and still on map
        else:
            map.draw_sand(coordinate)
            if coordinate == map.start:
                return False
            return True

    return False


def simulate_sand(filled, max_y):

    x, y = 500, 0

    while y <= max_y:
        if (x, y + 1) not in filled:
            y += 1
            continue

        if (x - 1, y + 1) not in filled:
            x -= 1
            y += 1
            continue

        if (x + 1, y + 1) not in filled:
            x += 1
            y += 1
            continue

        # Everything filled, come to rest
        filled.add((x, y))
        if (x, y) == (500, 0):
            return False
        return True

    return False


def solve_part_one(lines):
    rocks = parse(lines)

    map = Map(rocks=rocks, start=Coordinate(row=0, column=500))

    units_of_sand = 0

    while pour_unit_of_sand_from_source(map):
        units_of_sand += 1

    filled = set()
    filled.update([(c.column, c.row) for c in map.rocks])

    # while simulate_sand(filled, map.max_row):
    #     units_of_sand += 1

    # breakpoint()

    # map.print()

    return units_of_sand


def solve_part_two(lines):
    rocks = parse(lines)

    map = Map(rocks=rocks, start=Coordinate(row=0, column=500))

    # add one line of rock
    line_of_rock = []

    required_width = 2 * (map.height + 2) + 1

    min_column = map.start.column - ((required_width - 1) // 2)
    max_column = map.start.column + ((required_width - 1) // 2)

    for column in range(min_column, max_column + 1):
        line_of_rock.append(Coordinate(row=map.max_row + 2, column=column))

    map.rocks.update(line_of_rock)
    map.calculate_size()

    map.max_row

    units_of_sand = 0

    # while pour_unit_of_sand_from_source(map):
    #     units_of_sand += 1

    filled = set()
    filled.update([(c.column, c.row) for c in map.rocks])

    while simulate_sand(filled, map.max_row):
        units_of_sand += 1

    # breakpoint()

    # map.print()

    return units_of_sand
