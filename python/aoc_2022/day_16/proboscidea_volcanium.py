import re
from dataclasses import dataclass
from typing import Optional

from aoc_2022.utils.utils import parse_positive_integers


@dataclass
class Valve:
    label: str
    flow_rate: int
    open: Optional[bool] = False
    neighbours: Optional[list["Valve"]] = None
    tunnels: Optional[list["Tunnel"]] = None


@dataclass
class Tunnel:
    distance: int
    valve: Valve


class ValvesState:
    def __init__(self, open_valve_labels: set[str]) -> None:
        self.open_valve_labels = open_valve_labels

    def is_valve_open(self, valve_label):
        return valve_label in self.open_valve_labels

    def open_valve(self, valve_label):
        open_valve_labels = self.open_valve_labels.copy()
        open_valve_labels.add(valve_label)
        return ValvesState(open_valve_labels)
        # self.open_valve_labels.add(valve_label)


def parse(lines: list[str]) -> dict[str, Valve]:
    neighbours = {}
    valves = {}

    for line in lines:
        labels = re.findall("[A-Z][A-Z]+", line)
        label = labels[0]
        neighbours_labels = labels[1:]

        flow_rate = parse_positive_integers(line)[0]

        valve = Valve(label=label, flow_rate=flow_rate)

        neighbours[label] = neighbours_labels
        valves[label] = valve

    for valve_label, neighbours_labels in neighbours.items():
        valves[valve_label].neighbours = [valves[label] for label in neighbours_labels]

    distances = determine_distances(valves=valves)

    for label, neighbour_distances in distances.items():
        valve = valves[label]
        valve.tunnels = []
        for neighbour_label, neighbour_distance in neighbour_distances.items():
            neighbour = valves[neighbour_label]
            tunnel = Tunnel(distance=neighbour_distance, valve=neighbour)
            valve.tunnels.append(tunnel)

    return valves


def determine_distances(valves: dict[str, Valve]):
    from collections import deque

    distances = {}

    # loop over all valves
    for label, valve in valves.items():

        distances[label] = {}
        visited = {label}

        queue = deque([(0, valve)])

        print(f"Find routes for {label}")

        # calculate distance for every valve this valve can reach
        while queue:
            distance, valve = queue.popleft()

            print(distance, valve.label)

            for neighbour in valve.neighbours:

                # this assumes the first route was shorter?
                if neighbour.label in visited:
                    continue

                visited.add(neighbour.label)

                # store distance if valve not blocked
                if neighbour.flow_rate != 0:
                    distances[label][neighbour.label] = distance + 1

                queue.append((distance + 1, neighbour))

    return distances


# keep track of combinations of open valves
cache = {}


def depth_first_search(time, valve: Valve, state: ValvesState):

    if (time, valve.label, hash(state)) in cache:
        return cache[time, valve.label, hash(state)]

    pressure_release = 0

    for tunnel in valve.tunnels:

        if state.is_valve_open(tunnel.valve.label):
            continue

        time_remaining = time - tunnel.distance - 1

        # we can't reach this valve or opening it has no effect since the remaining time is 0
        if time_remaining <= 0:
            continue

        added_pressure_release = tunnel.valve.flow_rate * time_remaining

        pressure_release = max(
            pressure_release,
            depth_first_search(
                time_remaining, tunnel.valve, state.open_valve(tunnel.valve.label)
            )
            + added_pressure_release,
        )

    cache[time, valve.label, hash(state)] = pressure_release

    return pressure_release


class Puzzle:
    def __init__(self, minutes_left: int, valve: Valve) -> None:
        self.release_pressure_per_minute = 0
        self.total_released_pressure = 0
        self.minutes_left = minutes_left
        self.minute = 1
        self.valve = valve
        self.open_valves = []

    def __release_pressure(self):
        self.total_released_pressure += self.release_pressure_per_minute

    def solve(self):

        while self.minute <= self.minutes_left:

            print()
            print(f"== Minute {self.minute} ==")
            if len(self.open_valves) == 0:
                print("No valves are open.")
            elif len(self.open_valves) == 1:
                print(
                    f"Valve {self.open_valves[0].label} is open, releasing {self.release_pressure_per_minute} pressure."
                )
            else:
                valve_labels = ", ".join([valve.label for valve in self.open_valves])
                print(
                    f"Valves {valve_labels} are open, releasing {self.release_pressure_per_minute} pressure."
                )

            self.__release_pressure()

            # valve is closed and flow rate > 0
            if self.valve.open is False and self.valve.flow_rate > 5:
                self.open_valve()
            else:
                self.move_to_next_valve()

            self.minute += 1

    def open_valve(self):
        print(f"You open {self.valve.label}.")

        self.valve.open = True
        self.release_pressure_per_minute += self.valve.flow_rate

        self.open_valves.append(self.valve)

    def move_to_next_valve(self):

        num_neighbours = len(self.valve.neighbours)

        for index in range(num_neighbours):

            neighbour_valve = self.valve.neighbours[index]

            # if the valve is open we've already visited it
            if neighbour_valve.open is True:
                continue

            self.valve = neighbour_valve
            break

        print(f"You move to valve {self.valve.label}")


def solve_part_one(lines: list[str], example: bool):
    valves = parse(lines)

    return depth_first_search(30, valves["AA"], ValvesState(set()))

    # valve = valves["AA"]

    # puzzle = Puzzle(minutes_left=30, valve=valve)

    # puzzle.solve()

    # return puzzle.total_released_pressure


def solve_part_two(lines: list[str], example: bool):
    pass
