N = (-1, 0)
NE = (-1, 1)
E = (0, 1)
SE = (1, 1)
S = (1, 0)
SW = (1, -1)
W = (0, -1)
NW = (-1, -1)


def parse(lines: list[str]):
    elves = []

    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char == "#":
                elves.append((row, column))

    return elves


def are_other_elves_around(elve, elves) -> dict[tuple[int, int], bool]:

    directions = (N, NE, E, SE, S, SW, W, NW)
    elves_around = {}

    for direction in directions:
        delta_row, delta_column = direction
        adjacent_position = elve[0] + delta_row, elve[1] + delta_column

        if adjacent_position in elves:
            elves_around[direction] = True
            continue

        elves_around[direction] = False

    return elves_around


def find_rectangle_containing_elves(elves):
    min_row = min(elves, key=lambda c: c[0])[0]
    max_row = max(elves, key=lambda c: c[0])[0]
    min_column = min(elves, key=lambda c: c[1])[1]
    max_column = max(elves, key=lambda c: c[1])[1]

    return min_row, min_column, max_row, max_column


def print_elves(elves):
    elve = "#"
    empty = "."

    rectangle = find_rectangle_containing_elves(elves)

    min_row, min_column, max_row, max_column = rectangle

    for row in range(min_row - 2, max_row + 3):
        line = []
        for column in range(min_column - 2, max_column + 3):
            if (row, column) in elves:
                line.append(elve)
            else:
                line.append(empty)
        print("".join(line))

    print()


def move_elves(elves, rounds=None, part_two=False):
    directions_to_consider = [
        (N, NE, NW),
        (S, SE, SW),
        (W, NW, SW),
        (E, NE, SE),
    ]

    # print_elves(elves)

    for round in range(1, rounds + 1):
        elve_positions = set(elves)
        proposed_positions = dict()

        # first halve, detemine proposed steps
        for elve_id, elve in enumerate(elves):
            # if no other elves are around, do nothing
            elves_around = are_other_elves_around(elve, elve_positions)

            if not any(elves_around.values()):
                continue

            proposed_position = None

            # propose step in first valid direction
            for directions in directions_to_consider:
                #
                for direction in directions:
                    if elves_around[direction] is True:
                        break
                # no elves in any direction
                else:
                    proposed_position = (
                        elve[0] + directions[0][0],
                        elve[1] + directions[0][1],
                    )
                    break

            if proposed_position is None:
                continue

            # if no other elve proposes this new position, add it
            if proposed_position not in proposed_positions:
                proposed_positions[proposed_position] = elve_id
            # if another elve already proposed this position, remove it
            else:
                proposed_positions.pop(proposed_position)

        # second halve, move
        moved_elves = 0

        for proposed_position, elve_id in proposed_positions.items():
            elves[elve_id] = proposed_position
            moved_elves += 1

        if part_two is True and moved_elves == 0:
            return round

        # rotate directions to consider
        directions_to_consider = directions_to_consider[1:] + directions_to_consider[:1]

        # print elves
        # print_elves(elves)
    return rounds


def solve_part_one(lines: list[str], example: bool) -> int:
    # lines = [
    #     ".....",
    #     "..##.",
    #     "..#..",
    #     ".....",
    #     "..##.",
    #     ".....",
    # ]

    elves = parse(lines)

    rounds = 10

    move_elves(elves=elves, rounds=rounds, part_two=False)

    elve_positions = set(elves)

    rectangle = find_rectangle_containing_elves(elves)

    min_row, min_column, max_row, max_column = rectangle

    empty_ground_tiles = 0

    for row in range(min_row, max_row + 1):
        for column in range(min_column, max_column + 1):
            if (row, column) not in elve_positions:
                empty_ground_tiles += 1

    return empty_ground_tiles


def solve_part_two(lines: list[str], example: bool) -> int:
    elves = parse(lines)

    rounds = 1_000_000

    round = move_elves(elves=elves, rounds=rounds, part_two=True)

    return round
