from dataclasses import dataclass
from enum import Enum, auto


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
                ".#",
                ".#",
                "##",
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

        for row in range(self.height):
            for column in range(self.width):
                if self.grid[row][column] == "#":
                    self.coordinates.add((row, column))

    def move_left(self):
        self.move((-1, 0))

    def move_right(self):
        self.move((1, 0))

    def move_down(self):
        self.move((0, 1))

    def move(self, offset):
        row_offset, column_offset = offset

        new_coordinates = set()
        for row, column in self.coordinates:
            new_coordinates.add((row + row_offset, column + column_offset))

        self.coordinates = new_coordinates

    def __str__(self):
        return "\n".join(self.grid)


class Chamber:
    def __init__(self, width, height, jet_pattern, start_offset) -> None:
        self.width = width
        self.height = height
        self.jet_pattern = jet_pattern
        self.start_offset = start_offset

        self.grid = [["."] * self.width for _ in range(self.height)]

        self.walls = set()

        for row in range(self.height):
            for column in range(self.width):
                if row == 0:
                    self.walls.add((row, column))
                    continue
                if column == 0:
                    self.walls.add((row, column))
                    continue
                if column == self.width - 1:
                    self.walls.add((row, column))

        self.rocks = set()

        self._jet_index = 0
        self.rock = None
        self.bottom_row = self.height - 1

    def add_rock(self, rock: Rock):
        self.rock = rock

        self.rock.move(self.start_offset)

    def push_rock_by_jet(self):
        jet = self.jet_pattern[self._jet_index % len(self.jet_pattern)]

        self._jet_index += 1

        previous_coordinates = self.rock.coordinates

        if jet == ">":
            self.rock.move_right()

        elif jet == "<":
            self.rock.move_left()

        # check if we hit something
        if self.rock.coordinates.intersection(self.walls):
            self.rock.coordinates = previous_coordinates
            return

        if self.rock.coordinates.intersection(self.rocks):
            self.rock.coordinates = previous_coordinates
            return

    def move_rock_down(self):

        previous_coordinates = self.rock.coordinates

        self.rock.move_down()

        # check if we hit something
        if self.rock.coordinates.intersection(self.walls):
            self.rock.coordinates = previous_coordinates
            return

        if self.rock.coordinates.intersection(self.rocks):
            self.rock.coordinates = previous_coordinates
            return

        # check if we can move down

        # ideas
        # make all rock coordinates a set
        # make chamber walls also a set
        # perhaps even merge those

    def rock_had_come_to_rest(self):
        pass


def solve_part_one(lines: list[str], example: bool):
    number_of_rocks = 2200
    chamber_width = 7
    chamber_height = number_of_rocks * 4
    start_offset = PositionOffset(row=3, column=2)

    jet_pattern = lines[0]

    generator = RockGenerator()
    chamber = Chamber(
        width=chamber_width,
        height=chamber_height,
        jet_pattern=jet_pattern,
        start_offset=start_offset,
    )

    for rock in generator.rocks(number_of_rocks):

        chamber.add_rock(rock)

        # while rock has not come to rest
        while not chamber.rock_had_come_to_rest():

            # pushed by jet
            chamber.push_rock_by_jet()

            # fall down
            chamber.move_rock_down()


def solve_part_two(lines: list[str], example: bool):
    pass
