import logging
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Generator

logger = logging.getLogger()


class Map:
    def __init__(self, grid: list[list[int]], start, end) -> None:
        self.grid = grid
        self.start = start
        self.end = end
        self.rows = len(grid)
        self.columns = len(grid[0])
        self.visited = [[False] * self.columns for _ in range(self.rows)]

    def visit(self, row, column):
        self.visited[row][column] = True

    def have_visited(self, row, column):
        return self.visited[row][column]

    def is_on_map(self, row, column):

        if not (0 <= row < self.rows):
            return False

        if not (0 <= column < self.columns):
            return False

        return True

    def is_end(self, row, column):
        return (row, column) == self.end

    def determine_destinations(
        self, row, column, direction
    ) -> Generator[tuple[int], None, None]:
        UP = -1, 0
        RIGHT = 0, 1
        DOWN = 1, 0
        LEFT = 0, -1

        for delta_row, delta_column in [UP, RIGHT, DOWN, LEFT]:
            destination_row = row + delta_row
            destination_column = column + delta_column

            if not self.is_on_map(destination_row, destination_column):
                continue

            destination_height = self.grid[destination_row][destination_column]
            current_height = self.grid[row][column]

            if direction == "up" and (destination_height - current_height) <= 1:
                yield destination_row, destination_column

            if direction == "down" and (destination_height - current_height) >= -1:
                yield destination_row, destination_column

    def find_positions_with_height(self, height):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.grid[row][column] == height:
                    yield row, column

    def reset_visited(self):
        self.visited = [[False] * self.columns for _ in range(self.rows)]


@dataclass
class Location:
    distance: int
    row: int
    column: int


def determine_height(char) -> int:
    ASCII_OFFSET_LOWERCASE_A = 97

    if char == "S":
        return 0

    if char == "E":
        return 25

    return ord(char) - ASCII_OFFSET_LOWERCASE_A


def parse_height_map(lines) -> Map:
    START_MARKER = "S"
    END_MARKER = "E"
    grid = []
    for row, line in enumerate(lines):
        if START_MARKER in line:
            start = (row, line.index("S"))

        if END_MARKER in line:
            end = (row, line.index("E"))

        heights = [determine_height(char) for char in line]

        grid.append(heights)

    return Map(grid=grid, start=start, end=end)


def find_shortest_path(map: Map, start, is_end, direction="up"):
    # dijkstra ?

    heap = []

    heappush(heap, (0, start[0], start[1]))

    logger.debug(f"Find shortest path from {start}.")

    while True:
        distance, row, column = heappop(heap)

        if map.have_visited(row, column) and len(heap) == 0:
            logger.debug(f"No route to end possible for start {start}")
            return None

        if map.have_visited(row, column):
            continue

        map.visit(row, column)

        if is_end(row, column, map):
            return distance

        for destination in map.determine_destinations(row, column, direction):
            heappush(heap, (distance + 1, destination[0], destination[1]))


def solve_part_one(lines: list[str], example: bool) -> int:
    map = parse_height_map(lines)

    # we finish
    def is_end(row, column, map):
        return (row, column) == map.end

    return find_shortest_path(map, map.start, is_end)


def solve_part_two(lines: list[str], example: bool) -> int:
    map = parse_height_map(lines)

    # we finish when we found a tile with height = 0
    def is_end(row, column, map: Map):
        return map.grid[row][column] == 0

    # this time we start at the end and traverse backwards for better performance
    distance = find_shortest_path(map, start=map.end, is_end=is_end, direction="down")

    return distance


def solve_part_two_brute_force(lines):
    map = parse_height_map(lines)
    path_lengths = []

    def is_end(row, column, map):
        return (row, column) == map.end

    for row, column in map.find_positions_with_height(determine_height("a")):
        distance = find_shortest_path(map, start=(row, column), is_end=is_end)
        if distance is not None:
            path_lengths.append(distance)
        map.reset_visited()
