import logging

logger = logging.getLogger()

rock_symbol = "🟫"
air_symbol = "⬛"
source_symbol = "🟦"
sand_symbol = "🟨"


def convert_line_to_coordinates(start, end):
    """Convert a line given by a start and end coordinate to a list of coordinates"""

    coordinates = []
    start_row, start_column = start
    end_row, end_column = end

    # horizontal line
    if start_row == end_row:
        # if line is right to left -> swap
        if start_column > end_column:
            (start_row, start_column), (end_row, end_column) = end, start

        for column in range(start_column, end_column + 1):
            coordinates.append((start_row, column))

        return coordinates

    # vertical line
    if start_column == end_column:
        # if line is bottom to top -> swap
        if start_row > end_row:
            (start_row, start_column), (end_row, end_column) = end, start

        for row in range(start_row, end_row + 1):
            coordinates.append((row, start_column))

        return coordinates

    raise ValueError("Start and end coordinates should be horizontal or vertical")


def parse_cave(lines):

    cave = {}

    for line in lines:
        numbers = [int(element) for element in line.replace(" -> ", ",").split(",")]
        for i in range(0, len(numbers) - 2, 2):
            start = numbers[i + 1], numbers[i]
            end = numbers[i + 3], numbers[i + 2]
            coordinates = convert_line_to_coordinates(start, end)
            for c in coordinates:
                cave[c] = rock_symbol

    return cave


def drop_unit_of_sand(cave, source, max_row):

    row, column = source

    while row <= max_row:

        # down one step
        if (row + 1, column) not in cave:
            row += 1
            continue
        # down and to the left one step
        if (row + 1, column - 1) not in cave:
            row += 1
            column -= 1
            continue
        # down and to the right one step
        if (row + 1, column + 1) not in cave:
            row += 1
            column += 1
            continue

        # comes to rest
        cave[(row, column)] = sand_symbol

        # blocking the source
        if (row, column) == source:
            return False

        return True

    # fall into the endless void
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

            line.append(air_symbol)
        printer("".join(line))


def add_floor(cave, source):
    rows = [coordinate[0] for coordinate in cave]
    max_row = max(rows)
    height = max_row + 1

    required_width = 2 * (height + 2) + 1

    min_column = source[1] - ((required_width - 1) // 2)
    max_column = source[1] + ((required_width - 1) // 2)

    for column in range(min_column, max_column + 1):
        cave[(max_row + 2, column)] = rock_symbol

    return cave


def solve_part_one(lines):
    source = 0, 500

    cave = parse_cave(lines)

    cave[source] = source_symbol

    max_row = max([coordinate[0] for coordinate in cave])

    units_of_sand = 0

    while drop_unit_of_sand(cave, source=source, max_row=max_row):
        units_of_sand += 1

    if logger.level == logging.DEBUG:
        print_cave(cave)

    return units_of_sand


def solve_part_two(lines):
    source = 0, 500

    cave = parse_cave(lines)

    cave = add_floor(cave=cave, source=source)

    max_row = max([coordinate[0] for coordinate in cave])

    units_of_sand = 0

    while drop_unit_of_sand(cave, source=source, max_row=max_row):
        units_of_sand += 1

    if logger.level == logging.DEBUG:
        print_cave(cave)

    return units_of_sand + 1
