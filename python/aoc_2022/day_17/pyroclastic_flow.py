import logging
from dataclasses import dataclass
from enum import Enum, auto

logger = logging.getLogger(__file__)


class RockType(Enum):
    I_HORIZONTAL = auto()
    X = auto()
    J = auto()
    I_VERTICAL = auto()
    O = auto()


class RockGenerator:

    ROCK_TYPE_ORDER = [
        RockType.I_HORIZONTAL,
        RockType.X,
        RockType.J,
        RockType.I_VERTICAL,
        RockType.O,
    ]
    NUM_ROCK_TYPES = 5

    def __init__(self) -> None:
        self.__rock_type_index = 0

    def rocks(self, number_of_rocks):
        for _ in range(number_of_rocks):
            yield self.next_rock()

    def next_rock(self):
        rock_type = self.ROCK_TYPE_ORDER[self.__rock_type_index % self.NUM_ROCK_TYPES]

        self.__rock_type_index += 1

        if rock_type is RockType.I_HORIZONTAL:
            grid = ["####"]
            return Rock(grid)

        if rock_type is RockType.X:
            grid = [
                ".#.",
                "###",
                ".#.",
            ]
            return Rock(grid)

        if rock_type is RockType.J:
            grid = [
                "..#",
                "..#",
                "###",
            ]
            return Rock(grid)

        if rock_type is RockType.I_VERTICAL:
            grid = [
                "#",
                "#",
                "#",
                "#",
            ]
            return Rock(grid)

        if rock_type is RockType.O:
            grid = [
                "##",
                "##",
            ]
            return Rock(grid)


class Jet:
    LEFT = "<"
    RIGHT = ">"


@dataclass
class Position:
    row: int
    column: int

    def __iter__(self):
        yield self.row
        yield self.column


class PositionOffset(Position):
    pass


class Rock:
    def __init__(self, grid):
        self.width = len(grid[0])
        self.height = len(grid)
        self.grid = grid
        self.coordinates = set()
        self.previous_coordinates = set()

        # store coordinates
        for row in range(self.height):
            for column in range(self.width):
                if self.grid[row][column] == "#":
                    self.coordinates.add((row, column))
                    self.previous_coordinates.add((row, column))

    def roll_back(self):
        self.coordinates = self.previous_coordinates

    def move_left(self):
        self.move((0, -1))

    def move_right(self):
        self.move((0, 1))

    def move_down(self):
        self.move((1, 0))

    def move(self, offset):
        row_offset, column_offset = offset

        new_coordinates = set()
        for row, column in self.coordinates:
            new_coordinates.add((row + row_offset, column + column_offset))

        self.previous_coordinates = self.coordinates
        self.coordinates = new_coordinates

    def __str__(self):
        return "\n".join(self.grid)


class Chamber:
    def __init__(
        self, width, height, jet_pattern, start_offset: PositionOffset
    ) -> None:
        self.width = width
        self.height = height
        self.jet_pattern = jet_pattern

        # self.start_offset = PositionOffset(
        #     row=self.height - start_offset.row, column=start_offset.column
        # )

        self.grid = [["."] * self.width for _ in range(self.height)]

        self.walls = set()

        for row in range(self.height):
            for column in range(self.width):
                if row == (self.height - 1):
                    self.walls.add((row, column))
                    self.grid[row][column] = "-"
                    continue
                if column in [0, (self.width - 1)]:
                    self.walls.add((row, column))
                    self.grid[row][column] = "|"
                    continue

        self.grid[self.height - 1][0] = "+"
        self.grid[self.height - 1][self.width - 1] = "+"

        self.rocks = set()

        self._jet_index = 0
        self._rock_came_to_rest = False
        self.rock = None
        self.bottom_row = self.height - 1

    def add_rock(self, rock: Rock):
        self._rock_came_to_rest = False
        self.rock = rock

        # highest rock or wall + 4
        if len(self.rocks) == 0:
            row_offset = (self.height - 1) - 3
        else:
            row_offset = min(self.rocks, key=lambda coordinate: coordinate[0])[0] - 3

        # offset is bottom left
        column_offset = 3

        # TODO this assumes the rock is at position 0,0 top left
        self.rock.move((row_offset - self.rock.height, column_offset))

    def push_rock_by_jet(self):
        jet = self.jet_pattern[self._jet_index % len(self.jet_pattern)]

        self._jet_index += 1

        if jet == ">":
            logger.debug("Jet of gas pushed rock to the right:")
            self.rock.move_right()

        elif jet == "<":
            logger.debug("Jet of gas pushed rock to the left:")
            self.rock.move_left()

        # check if we hit something
        if self.rock.coordinates.intersection(self.walls):
            self.rock.roll_back()
            return

        if self.rock.coordinates.intersection(self.rocks):
            self.rock.roll_back()
            return

    def move_rock_down(self):

        self.rock.move_down()

        # check if we hit any other other
        if self.rock.coordinates.intersection(self.rocks):
            self.rock.roll_back()
            self.rocks.update(self.rock.coordinates)
            self._rock_came_to_rest = True
            self.rock = None
            # update start offset
            return

        # check if we hit the wall (including bottomg)
        if self.rock.coordinates.intersection(self.walls):
            self.rock.roll_back()
            self.rocks.update(self.rock.coordinates)
            self._rock_came_to_rest = True
            self.rock = None
            logger.debug("Rock falls 1 unit, causing it to come to rest:")
            return

        logger.debug("Rock falls 1 unit:")

    def did_rock_came_to_rest(self):
        return self._rock_came_to_rest

    def print(self, printer):
        return

        # if we have a falling rock use that as start
        if self.rock:
            row_start = min(
                self.rock.coordinates, key=lambda coordinate: coordinate[0]
            )[0]
        # if we have no falling rock or rocks use the bottom wall as start
        elif len(self.rocks) == 0:
            row_start = self.height - 4
        # else use the heighst rock as start
        else:
            row_start = min(self.rocks, key=lambda coordinate: coordinate[0])[0]

        # start printing at top rock (falling or resting)
        for row in range(row_start, self.height):

            line = [" "] * self.width

            for column in range(self.width):
                # add falling rocks
                if (row, column) in self.rocks:
                    line[column] = "#"
                # add rocks
                elif self.rock is not None and (row, column) in self.rock.coordinates:
                    line[column] = "@"
                else:
                    line[column] = self.grid[row][column]

            printer("".join(line))

        printer("")

    def get_height_tower_of_rocks(self):
        min_row = min(self.rocks, key=lambda coordinate: coordinate[0])[0]
        return self.height - min_row - 1


def solve_part_one(lines: list[str], example: bool):
    number_of_rocks = 2022
    chamber_width = 7 + 2
    chamber_height = number_of_rocks * 4
    start_offset = PositionOffset(row=3 + 1, column=2 + 1)

    jet_pattern = lines[0]

    generator = RockGenerator()

    chamber = Chamber(
        width=chamber_width,
        height=chamber_height,
        jet_pattern=jet_pattern,
        start_offset=start_offset,
    )

    for i, rock in enumerate(generator.rocks(number_of_rocks)):

        chamber.add_rock(rock)

        if i == 0:
            logger.debug("The first rock begins falling:")
        else:
            logger.debug("A new rock begins falling:")

        chamber.print(printer=logger.debug)

        # while rock has not come to rest
        while not chamber.did_rock_came_to_rest():

            # pushed by jet
            chamber.push_rock_by_jet()

            chamber.print(printer=logger.debug)

            # fall down
            chamber.move_rock_down()

            chamber.print(printer=logger.debug)

    return chamber.get_height_tower_of_rocks()


def solve_part_two(lines: list[str], example: bool):
    pass
