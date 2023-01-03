# every turn all the blizzards move one position in the given direction
#     n, e, s, w

#     keep track of all blizzard positions
#     keep track of all blizzard types (n, e, s, w)
#     multiple blizzards can share the same location

#     for every posible move we need to check if we collide with a blizzard

#     max blizzards is around 3000


#     set of blizard positions can't work since non unique
#         at least blizzards with different directions can overlap
#         but not when they have the same direction
#     list of blizzards, position,


from dataclasses import dataclass
from heapq import heappop, heappush

N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)


def parse(lines: list[str]):
    # find initial location of the blizzards
    valley: dict[str, set[tuple[int, int]]] = {
        "^": set(),
        ">": set(),
        "v": set(),
        "<": set(),
        "#": set(),
        # ".": set(),
    }
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char == ".":
                continue
            valley[char].add((row, column))

    max_row = len(lines)
    max_column = len(lines[0])

    return valley, (max_row, max_column)


# @dataclass
# class ValleyState:
#     blizzard_north: set[tuple[int, int]]


class Valley:
    def __init__(self, initial_state, max_row, max_column) -> None:
        self.valley_state = {0: initial_state}
        self.max_row = max_row
        self.max_column = max_column

    def state_at_time(self, time):
        if time in self.valley_state:
            return self.valley_state[time]

        previous_state = self.valley_state[time - 1]

        next_state: dict[str, set[tuple[int, int]]] = {
            "^": set(),
            ">": set(),
            "v": set(),
            "<": set(),
            "#": previous_state["#"],
        }

        for tile_type, coordinates in previous_state.items():
            if tile_type == "^":
                next_state[tile_type] = self._move_up(coordinates)
            if tile_type == ">":
                next_state[tile_type] = self._move_right(coordinates)
            if tile_type == "v":
                next_state[tile_type] = self._move_down(coordinates)
            if tile_type == "<":
                next_state[tile_type] = self._move_left(coordinates)

        self.valley_state[time] = next_state

        return next_state

    def _move_up(self, coordinates):
        return self._move(coordinates, -1, 0)

    def _move_right(self, coordinates):
        return self._move(coordinates, 0, 1)

    def _move_down(self, coordinates):
        return self._move(coordinates, 1, 0)

    def _move_left(self, coordinates):
        return self._move(coordinates, 0, -1)

    def _move(self, coordinates, delta_row, delta_column):
        new_coordinates = [None] * len(coordinates)

        for index, (row, column) in enumerate(coordinates):

            new_row, new_column = (row + delta_row, column + delta_column)

            if new_row == 0:
                new_row = self.max_row - 1

            if new_row == self.max_row:
                new_row = 1

            if new_column == 0:
                new_column = self.max_column - 1

            if new_column == self.max_column:
                new_column = 1

            new_coordinates[index] = new_row, new_column

        return set(new_coordinates)


def determine_next_positions(position, valley_state, start):

    for move in [N, E, S, W]:
        posible_next_position = position[0] + move[0], position[1] + move[1]
        if posible_next_position == start:
            continue
        if posible_next_position in valley_state["^"]:
            continue
        if posible_next_position in valley_state[">"]:
            continue
        if posible_next_position in valley_state["v"]:
            continue
        if posible_next_position in valley_state["<"]:
            continue
        if posible_next_position in valley_state["#"]:
            continue
        if posible_next_position[0] < 0:
            continue
        yield posible_next_position


def solve_dijkstra(start, end, valley: Valley):

    heap = []

    visited = set()

    heappush(heap, (0, 0, start[0], start[1]))

    print(f"start = {start}, end = {end}")

    while True:
        time, steps, row, column = heappop(heap)

        print(time, steps, row, column)
        # if time == 5:
        #     breakpoint()

        if (row, column, time) in visited:
            continue

        visited.add((row, column, time))

        # we found the exit
        if (row, column) == end:
            return time

        # get next valley state
        next_valley_state = valley.state_at_time(time + 1)

        # add state when we wait
        heappush(heap, (time + 1, steps, row, column))

        # determine where to go next
        for new_row, new_column in determine_next_positions(
            (row, column), next_valley_state, start
        ):
            print("\tadd new position", new_row, new_column)
            heappush(heap, (time + 1, steps + 1, new_row, new_column))

    return None


def solve_part_one(lines: list[str], example: bool) -> int:
    state, (max_row, max_column) = parse(lines)

    start = (0, 1)
    end = (max_row, max_column - 1)

    valley = Valley(initial_state=state, max_row=max_row, max_column=max_column)

    return solve_dijkstra(start=start, end=end, valley=valley)


def solve_part_two(lines: list[str], example: bool) -> int:
    pass
