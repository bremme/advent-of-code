import logging
import re
from enum import Enum

open_tile = "."
wall_tile = "#"
no_tile = " "


logger = logging.getLogger()


class Direction(Enum):
    R = 0
    D = 1
    L = 2
    U = 3

    @staticmethod
    def from_name(name):
        number_directions = {"R": 0, "D": 1, "L": 2, "U": 3}
        return Direction(number_directions[name])


direction_symbols = {"R": ">", "D": "v", "L": "<", "U": "^"}

number_directions = {0: "R", 1: "D", 2: "L", 3: "U"}

number_directions = {"R": 0, "D": 1, "L": 2, "U": 3}

symbol_numbers = {0: ">", 1: "v", 2: "<", 3: "^"}


def parse(lines):

    description = lines.pop()

    path_to_follow = []

    for move in re.split("([URDL])", description):
        if move.isnumeric():
            path_to_follow.append(int(move))
            continue
        path_to_follow.append(Direction(number_directions[move]))

    # pop empty line
    lines.pop()

    columns = len(max(lines, key=len))
    rows = len(lines)

    board = [[no_tile] * columns for _ in range(rows)]

    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            board[row][column] = char

    return board, path_to_follow


def print_board(grid, printer):
    for row in grid:
        printer("".join(row))


def determine_new_position(position, direction: Direction, max_row, max_column):
    row, column = position

    if direction == Direction.R and column < max_column:
        return row, column + 1

    if direction == Direction.R and column == max_column:
        return row, 0

    if direction == Direction.D and row < max_row:
        return row + 1, column

    if direction == Direction.D and row == max_row:
        return 0, column

    if direction == Direction.L and column > 0:
        return row, column - 1

    if direction == Direction.L and column == 0:
        return row, max_column

    if direction == Direction.U and row > 0:
        return row - 1, column

    if direction == Direction.U and row == 0:
        return max_row, column


def move_on_board(position, direction, steps, board) -> bool:

    max_row = len(board) - 1
    max_column = len(board[0]) - 1

    last_valid_position = position

    while steps > 0:

        while True:
            row, column = determine_new_position(
                position, direction, max_row=max_row, max_column=max_column
            )

            tile = board[row][column]

            if tile != no_tile:
                break

            position = row, column

        # return we hit a wall
        if tile == wall_tile:
            return last_valid_position

        # open tile, move and descrease steps
        if tile == open_tile or tile in ">v<^":
            board[row][column] = direction_symbols[direction.name]
            position = row, column
            last_valid_position = position
            steps -= 1
            continue

    return row, column


def change_direction(direction: Direction, turn: Direction) -> Direction:

    if turn is Direction.R:
        return Direction((direction.value + 1) % 4)

    if turn is Direction.L:
        return Direction((direction.value - 1) % 4)


def calculate_final_password(position, direction):
    row, column = position
    return 1000 * (row + 1) + 4 * (column + 1) + direction.value


def solve_part_one(lines, example):
    board, path_to_follow = parse(lines)
    # print_board(board, print)

    # determine start position
    row = 0
    column = 0

    for column in range(len(board[row])):
        if board[row][column] == open_tile:
            break

    position = row, column

    direction = Direction.R
    symbol = direction_symbols[direction.name]

    board[row][column] = symbol

    for move in path_to_follow:

        if type(move) is int:
            position = move_on_board(position, direction, steps=move, board=board)

        if type(move) is Direction:
            direction = change_direction(direction, turn=move)
            board[position[0]][position[1]] = direction_symbols[direction.name]

    print_board(board, logger.debug)

    return calculate_final_password(position, direction)


def solve_part_two(lines, example):
    pass
