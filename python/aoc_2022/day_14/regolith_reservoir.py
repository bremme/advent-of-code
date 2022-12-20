import logging

logger = logging.getLogger()

rock_symbol = "🟫"
air_symbol = "⬛"
source_symbol = "🟦"
sand_symbol = "🟨"


def line_coordinates(source, end):
    coordinates = []
    source_row, source_column = source
    end_row, end_column = end

    # horizontal line
    if source_row == end_row:
        # if line is right to left -> swap
        if source_column > end_column:
            (source_row, source_column), (end_row, end_column) = end, source

        for column in range(source_column, end_column + 1):
            coordinates.append((source_row, column))

        return coordinates

    # vertical line
    if source_column == end_column:
        # if line is bottom to top -> swap
        if source_row > end_row:
            (source_row, source_column), (end_row, end_column) = end, source

        for row in range(source_row, end_row + 1):
            coordinates.append((row, source_column))

        return coordinates

    raise ValueError("Start and end coordinates should be horizontal or vertical")


def parse(lines):

    cave = {}

    for line in lines:
        numbers = [int(element) for element in line.replace(" -> ", ",").split(",")]
        for i in range(0, len(numbers) - 2, 2):
            source = numbers[i + 1], numbers[i]
            end = numbers[i + 3], numbers[i + 2]
            coordinates = line_coordinates(source, end)
            for c in coordinates:
                cave[c] = rock_symbol

    return cave


def simulate_sand(cave, source, max_row):

    row, column = source

    while row <= max_row:
        if (row + 1, column) not in cave:
            row += 1
            # logger.debug(f"move down to {row}, {column}")
            continue

        if (row + 1, column - 1) not in cave:
            row += 1
            column -= 1
            # logger.debug(f"move down and left to {row}, {column}")
            continue

        if (row + 1, column + 1) not in cave:
            row += 1
            column += 1
            # logger.debug(f"move down and down and right to {row}, {column}")
            continue

        # Everrowthing filled, come to rest
        # logger.debug(f"came to rest {row}, {column}")
        # cave.add((row, column))
        cave[(row, column)] = sand_symbol

        if (row, column) == source:
            return False
        return True

    return False


def print_cave(cave, printer=print):

    rows = [coordinate[0] for coordinate in cave]
    columns = [coordinate[1] for coordinate in cave]
    min_row, max_row = 0, max(rows)
    min_column, max_column = min(columns), max(columns)
    width = max_column - min_column + 1
    height = max_row - min_row + 1

    for row in range(height):
        line = []
        for column in range(width):
            coordinate = row + min_row, column + min_column

            if coordinate in cave:
                line.append(cave[coordinate])
                continue

            # if coordinate in self.sand:
            #     line.append(sand_symbol)
            #     continue

            # if coordinate == self.source:
            #     line.append(source_symbol)
            #     continue

            line.append(air_symbol)
        printer("".join(line))


def add_floor(cave, source):
    rows = [coordinate[0] for coordinate in cave]
    max_row = max(rows)
    height = max_row + 1

    # add one line of rock
    line_of_rock = []

    required_width = 2 * (height + 2) + 1

    min_column = source[1] - ((required_width - 1) // 2)
    max_column = source[1] + ((required_width - 1) // 2)

    for column in range(min_column, max_column + 1):
        line_of_rock.append((max_row + 2, column))

    for c in line_of_rock:
        cave[c] = rock_symbol

    return cave


def solve_part_one(lines):
    source = 0, 500

    cave = parse(lines)

    cave[source] = source_symbol

    max_row = max([coordinate[0] for coordinate in cave])

    units_of_sand = 0

    while simulate_sand(cave, source=source, max_row=max_row):
        units_of_sand += 1

    if logger.level == logging.DEBUG:
        print_cave(cave)

    return units_of_sand


def solve_part_two(lines):
    source = 0, 500

    cave = parse(lines)

    cave = add_floor(cave=cave, source=source)

    max_row = max([coordinate[0] for coordinate in cave])

    units_of_sand = 0

    while simulate_sand(cave, source=source, max_row=max_row):
        units_of_sand += 1

    if logger.level == logging.DEBUG:
        print_cave(cave)

    return units_of_sand + 1
