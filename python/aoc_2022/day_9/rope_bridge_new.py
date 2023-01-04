N = (-1, 0)
NE = (-1, 1)
E = (0, 1)
SE = (1, 1)
S = (1, 0)
SW = (1, -1)
W = (0, -1)
NW = (-1, -1)
X = None


TAIL_DIRECTIONS = [
    [X, SE, S, SW, X],
    [SE, X, X, X, SW],
    [E, X, X, X, W],
    [NE, X, X, X, NW],
    [X, NE, N, NW, X],
]


def parse(lines: list[str]):
    DIRECTION_LOOKUP = {"U": N, "R": E, "D": S, "L": W}

    motions = []
    for line in lines:
        direction = DIRECTION_LOOKUP[line.split(" ")[0]]
        steps = int(line.split()[1])
        motions.append((direction, steps))

    return motions


def determine_tail_movement(head, tail):
    # determine tail movement
    delta_row, delta_column = tail[0] - head[0], tail[1] - head[1]

    row, column = delta_row + 2, delta_column + 2

    # tail is 2 left  of head     0, -2     -> E (move right)
    # tail is 2 up    of head    -2,  0     -> S (move down)
    # tail is 2 down  of head     2,  0     -> N (move up)
    # tail is 2 right of head     0,  2     -> W (move left)

    return TAIL_DIRECTIONS[row][column]


def solve_part_one(lines: list[str], example: bool) -> int:

    motions = parse(lines)
    tail_positions = set()

    start = 0, 0

    head = start
    tail = start

    tail_positions.add(tail)

    for head_move, steps in motions:

        # move
        for _ in range(steps):
            # move head
            head = head[0] + head_move[0], head[1] + head_move[1]

            tail_move = determine_tail_movement(head, tail)

            if not tail_move:
                continue

            tail = tail[0] + tail_move[0], tail[1] + tail_move[1]

            tail_positions.add(tail)

    return len(tail_positions)


def solve_part_two(lines: list[str], example: bool) -> int:
    number_of_knots = 10

    motions = parse(lines)
    tail_positions = set()

    start = 0, 0

    head = start
    tails = [start] * (number_of_knots - 1)

    tail_positions.add(tail)

    for head_move, steps in motions:

        # move
        for _ in range(steps):
            # move head
            head = head[0] + head_move[0], head[1] + head_move[1]

            # move knots
            current_head = head

            for tail in tails:

                tail_move = determine_tail_movement(head=current_head, tail=tail)

                # move tail
                if tail_move:
                    tail = tail[0] + tail_move[0], tail[1] + tail_move[1]

                current_head = tail

            tail_positions.add(tail)

    return len(tail_positions)
