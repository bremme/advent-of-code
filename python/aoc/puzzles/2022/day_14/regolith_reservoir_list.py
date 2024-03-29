import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger()


@dataclass
class Movement:
    delta_row: int
    delta_column: int


class Move(Enum):
    DOWN = Movement(1, 0)
    DOWN_LEFT = Movement(1, -1)
    DOWN_RIGHT = Movement(1, 1)


@dataclass
class Point:
    row: int
    column: int

    @staticmethod
    def from_point(point):
        return Point(point.row, point.column)

    def move(self, movement: Movement):
        self.row += movement.delta_row
        self.column += movement.delta_column

    def __add__(self, move: Movement):
        return Point(
            row=self.row + move.delta_row, column=self.column + move.delta_column
        )

    def __sub__(self, move: Movement):
        return Point(
            row=self.row - move.delta_row, column=self.column - move.delta_column
        )


@dataclass
class Path:
    points: list[Point]

    def add_point(self, point: Point):
        self.points.append(point)
        self.__iter_index = 0

    @staticmethod
    def is_vertical(start, end):

        if start.row == end.row:
            return False

        if start.column == end.column:
            return True

        ValueError("Line should be horizontal or vertical")

    def pairs(self):
        for i in range(0, len(self.points) - 1):
            yield self.points[i], self.points[i + 1]

    def __iter__(self):
        self.__iter_index = 0
        return self

    def __next__(self):
        try:
            self.__iter_index += 1
            return self.points[self.__iter_index - 1]
        except IndexError:
            raise StopIteration


def parse(lines, add_floor=False):
    paths = []
    max_rows = 0
    min_columns, max_columns = None, 0

    for line in lines:
        numbers = [int(element) for element in line.replace(" -> ", ",").split(",")]
        path = Path(points=[])
        for i in range(0, len(numbers), 2):
            row = numbers[i + 1]
            column = numbers[i]

            # determine size of map
            if row > max_rows:
                max_rows = row

            if column > max_columns:
                max_columns = column
                if min_columns is None:
                    min_columns = max_columns

            elif column < min_columns:
                min_columns = column

            point = Point(row=row, column=column)
            path.add_point(point)

        paths.append(path)

    # determine map size
    num_rows = max_rows + 1
    num_columns = max_columns - min_columns + 1
    midpoint_offset = 0
    path_slice = slice(0, len(paths))

    if add_floor:
        # determine required width of floor
        max_rows += 2
        num_rows = max_rows + 1
        max_columns = min_columns + (2 * num_rows)

        floor = Path(
            points=[
                Point(row=max_rows, column=0),
                Point(row=max_rows, column=2 * num_rows),
            ]
        )

        num_rows = max_rows + 1
        num_columns = max_columns - min_columns + 1

        midpoint_offset = ((max_columns - min_columns) // 2) - (500 - min_columns)

        paths.append(floor)

    # apply column offset
    for path in paths[path_slice]:
        for point in path:
            point.column = point.column - min_columns + midpoint_offset

    map_size = (num_rows, num_columns)

    source = Point(row=0, column=(500 - min_columns) + midpoint_offset)

    logger.debug(f"Create map of size {map_size}")

    map = Map(
        map_size,
        source=source,
        rock_symbol="🟫",
        air_symbol="⬛",
        source_symbol="🟦",
        sand_symbol="🟨",
    )

    return paths, map


class Map:
    def __init__(
        self,
        size,
        source,
        rock_symbol="#",
        air_symbol=".",
        source_symbol="+",
        sand_symbol="o",
    ) -> None:
        self.rows, self.columns = size
        self.source = source
        self.rock_symbol = rock_symbol
        self.air_symbol = air_symbol
        self.source_symbol = source_symbol
        self.sand_symbol = sand_symbol
        self.grid = [[self.air_symbol] * self.columns for _ in range(self.rows)]

        self.grid[source.row][source.column] = source_symbol

    def draw_paths(self, paths: list[Path]):
        for path in paths:
            self.draw_path(path)

    def draw_path(self, path: Path):

        # loop over pair of points
        for start, end in path.pairs():
            if path.is_vertical(start, end):
                self.draw_vertical_line(start, end)
                continue
            self.draw_horizontal_line(start, end)

    def draw_vertical_line(self, start: Point, end: Point):
        # if line is bottom to top -> swap
        if start.row > end.row:
            start, end = end, start

        for row in range(start.row, end.row + 1):
            self.grid[row][start.column] = self.rock_symbol

    def draw_horizontal_line(self, start: Point, end: Point):
        # if line is right to left -> swap
        if start.column > end.column:
            start, end = end, start

        for column in range(start.column, end.column + 1):
            self.grid[start.row][column] = self.rock_symbol

    def draw_sand(self, sand: Point):
        self.grid[sand.row][sand.column] = self.sand_symbol

    def pour_unit_of_sand_from_source(self):
        # while the sand unit has not come to rest -> move
        sand = Point.from_point(self.source)

        posible_moves = Move.DOWN.value, Move.DOWN_LEFT.value, Move.DOWN_RIGHT.value

        while True:

            for move in posible_moves:

                new_sand = sand + move

                # finish this iteration when the sand pours off the map
                if self.is_on_map(new_sand) is False:
                    return False

                if self.is_air(new_sand):
                    sand = new_sand
                    break
            # not moved and still on map
            else:
                self.draw_sand(sand)
                if sand == self.source:
                    return False
                return True

    def is_air(self, point):
        return self.grid[point.row][point.column] == self.air_symbol

    def is_on_map(self, point):
        if not (0 <= point.row < self.rows):
            return False

        if not (0 <= point.column < self.columns):
            return False

        return True

    def add_row(self, row: list[str]):
        self.grid.append(row)
        self.rows += 1

    def print(self, printer=print):
        for row in range(self.rows):
            printer("".join(self.grid[row]))


def solve_part_one(lines: list[str], example: bool) -> int:
    paths, map = parse(lines)

    map.draw_paths(paths)

    map.print(logger.debug)
    units_of_sand = 0

    while map.pour_unit_of_sand_from_source():
        units_of_sand += 1

    map.print(logger.debug)

    return units_of_sand


def solve_part_two(lines: list[str], example: bool) -> int:

    paths, map = parse(lines, add_floor=True)

    map.draw_paths(paths)

    units_of_sand = 0

    while map.pour_unit_of_sand_from_source():
        units_of_sand += 1

    map.print(logger.debug)

    return units_of_sand + 1
