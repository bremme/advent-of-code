import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import Generator

from aoc_2022.day_14.regolith_reservoir_set import Coordinate

logger = logging.getLogger(__file__)


def min_row(coordinates):
    return min(coordinates, key=lambda coordinate: coordinate[0])[0]


def min_column(coordinates):
    return min(coordinates, key=lambda coordinate: coordinate[0])[0]


class SymbolName(Enum):
    ROCK = auto()
    ROCK_FALLING = auto()
    EMPTY = auto()
    WALL = auto()
    FLOOR = auto()
    CORNER = auto()


class SymbolSetSymbols(Enum):
    DEFAULT = {
        SymbolName.ROCK: "#",
        SymbolName.ROCK_FALLING: "@",
        SymbolName.EMPTY: ".",
        SymbolName.WALL: "|",
        SymbolName.FLOOR: "-",
        SymbolName.CORNER: "+",
    }
    COLORS = {
        SymbolName.ROCK: "🟩",
        SymbolName.ROCK_FALLING: "🟦",
        SymbolName.EMPTY: "⬛",
        SymbolName.WALL: "🟧",
        SymbolName.FLOOR: "🟥",
        SymbolName.CORNER: "⬜️",
    }


class SymbolSet:
    def __init__(self, symbols: SymbolSetSymbols) -> None:
        self.rock = symbols.value[SymbolName.ROCK]
        self.rock_falling = symbols.value[SymbolName.ROCK_FALLING]
        self.empty = symbols.value[SymbolName.EMPTY]
        self.wall = symbols.value[SymbolName.WALL]
        self.floor = symbols.value[SymbolName.FLOOR]
        self.corner = symbols.value[SymbolName.CORNER]


# ❌ ⭕️✅ ❎ 🌐 💠  🌀 💤 ⏩ ⏪ ⏫ ⏬ 🔼 🔽 🔘 🔴 🟠 🟡 🟢 🔵 🟣 ⚫️ ⚪️ 🟤 🔺 🔻 🔸 🔹 🔶 🔷 🔳 🔲 ▪️ ▫️ ◾️ ◽️ ◼️ ◻️ 🟥 🟧 🟨 🟩 🟦 🟪 ⬛️ ⬜️ 🟫


@dataclass
class Position:
    row: int
    column: int

    def __iter__(self):
        yield self.row
        yield self.column

    def __getitem__(self, index):
        if index == 0:
            return self.row
        if index == 1:
            return self.column

        raise IndexError("Index out of range")

    def __len__(self):
        return 2

    @staticmethod
    def from_tuple(position: tuple):
        return Position(row=position[0], column=position[1])


class PositionOffset(Position):
    pass


class Index:
    def __init__(self, rollover):
        self._index = -1
        self._rollover = rollover

    def next(self):
        self._index += 1

        if self._index == self._rollover:
            self._index = 0

        return self._index


class RockType(Enum):
    I_HORIZONTAL = auto()
    X = auto()
    J = auto()
    I_VERTICAL = auto()
    O = auto()


class Rock:
    def __init__(self, grid: list[list[str]], symbol: str):
        self.width = len(grid[0])
        self.height = len(grid)
        self.grid = grid
        self.coordinates: set[tuple[int, int]] = set()
        self.previous_coordinates = set()

        # store coordinates
        for row in range(self.height):
            for column in range(self.width):
                if self.grid[row][column] == symbol:
                    self.coordinates.add((row, column))

        self.previous_coordinates = self.coordinates.copy()

    def undo_move(self):
        self.coordinates = self.previous_coordinates

    def move_left(self):
        self.move((0, -1))

    def move_right(self):
        self.move((0, 1))

    def move_down(self):
        self.move((1, 0))

    def move(self, offset: tuple):
        row_offset, column_offset = offset

        new_coordinates = set()

        for row, column in self.coordinates:
            new_coordinates.add((row + row_offset, column + column_offset))

        self.previous_coordinates = self.coordinates
        self.coordinates = new_coordinates

    def move_to(self, position: Position):
        # move top left to given position
        row_offset = position[0] - min_row(self.coordinates)
        column_offset = position[1] - min_column(self.coordinates)

        return self.move((row_offset, column_offset))

    def __str__(self):
        return "\n".join(self.grid)


class RockGenerator:

    ROCK_TYPE_ORDER = [
        RockType.I_HORIZONTAL,
        RockType.X,
        RockType.J,
        RockType.I_VERTICAL,
        RockType.O,
    ]
    NUM_ROCK_TYPES = 5

    def __init__(self, symbol_set) -> None:
        self.symbol_set = symbol_set

        self._rock_type_index = Index(rollover=len(self.ROCK_TYPE_ORDER))

        default_rock_grids = {
            RockType.I_HORIZONTAL: ["####"],
            RockType.X: [
                ".#.",
                "###",
                ".#.",
            ],
            RockType.J: [
                "..#",
                "..#",
                "###",
            ],
            RockType.I_VERTICAL: [
                "#",
                "#",
                "#",
                "#",
            ],
            RockType.O: [
                "##",
                "##",
            ],
        }
        rock_grids = {}

        for rock_type, grid in default_rock_grids.items():
            new_grid = []
            for line in grid:
                new_grid.append(
                    line.replace("#", symbol_set.rock).replace(".", symbol_set.empty)
                )
            rock_grids[rock_type] = new_grid

        self._rock_grids = rock_grids

    def rocks(self, number_of_rocks) -> Generator[Rock, None, None]:
        for _ in range(number_of_rocks):
            yield self.next_rock()

    def next_rock(self) -> Rock:
        rock_type = self.ROCK_TYPE_ORDER[self._rock_type_index.next()]

        return self.generate_rock(rock_type=rock_type)

    def generate_rock(self, rock_type: RockType) -> Rock:

        return Rock(
            grid=self._rock_grids[rock_type],
            symbol=self.symbol_set.rock,
        )


class Jet:
    LEFT = "<"
    RIGHT = ">"


class Chamber:
    def __init__(self, width, height, jet_pattern, symbol_set) -> None:
        self.width = width
        self.height = height
        self.jet_pattern = jet_pattern
        self.symbol_set = symbol_set

        self.grid = [[symbol_set.empty] * self.width for _ in range(self.height)]

        self.walls = set()

        # draw wall's and floor
        for row in range(self.height):
            for column in range(self.width):
                if row == (self.height - 1):
                    self.walls.add((row, column))
                    self.grid[row][column] = symbol_set.floor
                    continue
                if column in [0, (self.width - 1)]:
                    self.walls.add((row, column))
                    self.grid[row][column] = symbol_set.wall
                    continue

        self.grid[self.height - 1][0] = symbol_set.corner
        self.grid[self.height - 1][self.width - 1] = symbol_set.corner

        self.rocks = set()

        self._jet_index = 0
        self._rock_came_to_rest = False
        self.rock = None
        self.previous_rock = None
        self.bottom_row = self.height - 1

        self.num_rocks = 0
        self.num_yet_roll_overs = 0

    def get_state_signature(self):

        rock_coordinates = set()

        if len(self.rocks) == 0:
            row_offset = self.height
        else:
            row_offset = min_row(self.rocks)

        for i, coordinate in enumerate(sorted(self.rocks)):
            rock_coordinates.add((coordinate[0] - row_offset, coordinate[1]))
            # get approximately 10 rocks
            if i == (10 * 4):
                break

        # get something hashable which describes the type of rock
        grid = "|".join(self.previous_rock.grid)

        # mix the type of rock the jet index and the ~last 10 rocks
        return grid, self._jet_index, frozenset(rock_coordinates)

    def add_rock(self, rock: Rock):

        self._rock_came_to_rest = False
        self.rock = rock
        self.num_rocks += 1

        # highest rock or wall - 3
        if len(self.rocks) == 0:
            row_offset = (self.height - 1) - 3
        else:
            row_offset = min_row(self.rocks) - 3

        # offset is bottom left
        column_offset = 3

        self.rock.move_to((row_offset - self.rock.height, column_offset))

    def push_rock_by_jet(self):
        jet = self.jet_pattern[self._jet_index]

        self._jet_index += 1

        if self._jet_index == len(self.jet_pattern):
            self.num_yet_roll_overs += 1
            self._jet_index = 0
            # print(f"rollover {self.num_yet_roll_overs}, {self.num_rocks}")

        if jet == ">":
            logger.debug("Jet of gas pushed rock to the right:")
            self.rock.move_right()

        elif jet == "<":
            logger.debug("Jet of gas pushed rock to the left:")
            self.rock.move_left()

        # check if we hit something
        if self.rock.coordinates.intersection(self.walls):
            self.rock.undo_move()
            return

        if self.rock.coordinates.intersection(self.rocks):
            self.rock.undo_move()
            return

    def move_rock_down(self):

        self.rock.move_down()

        # check if we hit any other other rock or the wall
        if self.rock.coordinates.intersection(
            self.rocks
        ) or self.rock.coordinates.intersection(self.walls):
            self.rock.undo_move()
            self.rocks.update(self.rock.coordinates)
            self._rock_came_to_rest = True
            self.previous_rock = self.rock
            self.rock = None
            logger.debug("Rock falls 1 unit, causing it to come to rest:")
            return

        logger.debug("Rock falls 1 unit:")

    def did_rock_came_to_rest(self):
        return self._rock_came_to_rest

    def print(self, printer):
        if not logger.isEnabledFor(logging.DEBUG):
            return

        # if we have a falling rock use the top as the start
        if self.rock:
            row_start = min_row(self.rock.coordinates)
        # if we have no falling rock or rocks use the bottom wall as start
        elif len(self.rocks) == 0:
            row_start = self.height - 1 - 3
        # else use the highest rock as start
        else:
            row_start = min_row(self.rocks)

        # start printing at top rock (falling or resting)
        for row in range(row_start, self.height):

            line = [" "] * self.width

            for column in range(self.width):
                # add rocks
                if (row, column) in self.rocks:
                    line[column] = self.symbol_set.rock
                # add falling rock
                elif self.rock is not None and (row, column) in self.rock.coordinates:
                    line[column] = self.symbol_set.rock_falling
                # add walls
                else:
                    line[column] = self.grid[row][column]

            printer("".join(line))

        printer("")

    def get_height_tower_of_rocks(self):
        min_row = min(self.rocks, key=lambda coordinate: coordinate[0])[0]
        return self.height - min_row - 1


def solve_part_one(lines: list[str], example: bool):
    max_rock_height = 4
    number_of_rocks = 2022
    chamber_width = 7 + 2
    chamber_height = number_of_rocks * max_rock_height

    jet_pattern = lines[0]

    symbols_set = SymbolSet(symbols=SymbolSetSymbols.COLORS)

    generator = RockGenerator(symbol_set=symbols_set)

    chamber = Chamber(
        width=chamber_width,
        height=chamber_height,
        jet_pattern=jet_pattern,
        symbol_set=symbols_set,
    )

    for i, rock in enumerate(generator.rocks(number_of_rocks)):

        chamber.add_rock(rock)

        # if i == 0:
        #     logger.debug("The first rock begins falling:")
        # else:
        #     logger.debug("A new rock begins falling:")

        # chamber.print(printer=logger.debug)

        # while rock has not come to rest
        while not chamber.did_rock_came_to_rest():

            # pushed by jet
            chamber.push_rock_by_jet()
            # chamber.print(printer=logger.debug)

            # fall down
            chamber.move_rock_down()
    chamber.print(printer=logger.debug)

    return chamber.get_height_tower_of_rocks()


def solve_part_two(lines: list[str], example: bool):
    max_rock_height = 4
    number_of_rocks = 10000
    chamber_width = 7 + 2
    chamber_height = number_of_rocks * max_rock_height

    jet_pattern = lines[0]

    symbols_set = SymbolSet(symbols=SymbolSetSymbols.COLORS)

    generator = RockGenerator(symbol_set=symbols_set)

    chamber = Chamber(
        width=chamber_width,
        height=chamber_height,
        jet_pattern=jet_pattern,
        symbol_set=symbols_set,
    )

    signatures = {}

    rocks_added = 0

    # find repeating cycles
    while True:

        rock = generator.next_rock()

        chamber.add_rock(rock)

        rocks_added += 1

        while not chamber.did_rock_came_to_rest():
            chamber.push_rock_by_jet()
            chamber.move_rock_down()

        # get and compare signature
        signature = chamber.get_state_signature()

        if signature in signatures:
            previous_rocks_added, previous_height = signatures[signature]
            rocks_cycle = rocks_added - previous_rocks_added
            print(
                f"found equal signature {rocks_added}, {previous_rocks_added} -> {rocks_cycle}"
            )
            break

        signatures[signature] = rocks_added, chamber.get_height_tower_of_rocks()

    # 3146
    height_cycle = chamber.get_height_tower_of_rocks() - previous_height

    rocks_left = 1_000_000_000_000 - rocks_added

    # how many cycles will fit into rocks left
    num_cycles = rocks_left // rocks_cycle

    # how many additional rocks do we have to drop
    new_rocks_left = rocks_left % rocks_cycle

    for rock in generator.rocks(new_rocks_left):

        chamber.add_rock(rock)

        while not chamber.did_rock_came_to_rest():
            chamber.push_rock_by_jet()
            chamber.move_rock_down()

    final_height = chamber.get_height_tower_of_rocks()

    return final_height + (num_cycles * height_cycle)
