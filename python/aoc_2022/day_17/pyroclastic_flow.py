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

    def __init__(self) -> None:
        self.__rock_type_index = 0

    def rocks(self, number_of_rocks):
        for _ in range(number_of_rocks):
            yield self.next_rock()

    def next_rock(self):
        if self.__rock_type_index >= len(self.ROCK_TYPE_ORDER):
            self.__rock_type_index = 0

        rock_type = self.ROCK_TYPE_ORDER[self.__rock_type_index]

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


class Rock:
    def __init__(self, grid):
        self.width = len(grid[0])
        self.height = len(grid)
        self.grid = grid

    def __str__(self):
        return "\n".join(self.grid)


class Chamber:
    def __init__(self, width, height, jet_pattern) -> None:
        self.width = width
        self.height = height
        self.jet_pattern = jet_pattern
        self.grid = [["."] * self.width for _ in range(self.height)]

    def add_rock(self, rock):
        pass

    def push_rock_by_jet(self, direction):
        pass

    def move_rock_down(self):
        pass

    def rock_had_come_to_rest(self):



def solve_part_one(lines: list[str], example: bool):
    number_of_rocks = 2200
    chamber_width = 7
    chamber_height = number_of_rocks * 4
    start_column_offset = 2
    start_row_offset = 3

    jet_pattern = lines[0]

    generator = RockGenerator()
    chamber = Chamber(width=chamber_width, height=chamber_height, jet_pattern=jet_pattern)



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


max height of chamber ?
2200 * 4 = 8800