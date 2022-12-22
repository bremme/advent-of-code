def parse(lines):

    description = lines.pop()

    # pop empty line
    lines.pop()

    columns = len(max(lines, key=len))
    rows = len(lines)

    grid = [[" "] * columns for _ in range(rows)]

    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            grid[row][column] = char

    return grid, description


def print_grid():
    pass


def solve_part_one(lines, example):
    grid, description = parse(lines)
    breakpoint()


def solve_part_two(lines, example):
    pass
