import re
from collections import deque
from dataclasses import dataclass
from typing import Optional

from aoc.utils.utils import parse_positive_integers


@dataclass
class Valve:
    label: str
    flow_rate: int
    open: Optional[bool] = False
    neighbours: Optional[list["Valve"]] = None
    tunnels: Optional[list["Tunnel"]] = None

    def __hash__(self):
        return hash(self.label)


@dataclass
class Tunnel:
    distance: int
    valve: Valve


class ValvesState:
    def __init__(self, open_valves: Optional[list[Valve]] = None) -> None:
        self.__open_valve_labels = (
            {valve.label for valve in open_valves} if open_valves else set()
        )

    @property
    def key(self):
        return "|".join(self.__open_valve_labels)

    def is_valve_open(self, valve: Valve):
        return valve.label in self.__open_valve_labels

    def open_valve(self, valve):
        self.__open_valve_labels.add(valve.label)

    @staticmethod
    def from_state(state: "ValvesState"):
        new_state = ValvesState()
        new_state.__open_valve_labels = state.__open_valve_labels.copy()
        return new_state


class PuzzleInputParser:
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

        # connect neighbours
        for valve_label, neighbours_labels in neighbours.items():
            valves[valve_label].neighbours = [
                valves[label] for label in neighbours_labels
            ]

        # calculate distances
        distances = PuzzleInputParser.calcualte_distances(valves=valves)

        # build tunnels
        for label, neighbour_distances in distances.items():
            valve = valves[label]
            valve.tunnels = []
            for neighbour_label, neighbour_distance in neighbour_distances.items():
                neighbour = valves[neighbour_label]
                tunnel = Tunnel(distance=neighbour_distance, valve=neighbour)
                valve.tunnels.append(tunnel)

        return valves

    @staticmethod
    def calcualte_distances(valves: dict[str, Valve]) -> dict[str, list[str]]:

        distances = {}

        # loop over all valves
        for label, valve in valves.items():

            distances[label] = {}
            visited = {label}

            queue = deque([(0, valve)])

            # calculate distance for every valve this valve can reach and has a flow rate > 0
            while queue:
                distance, valve = queue.popleft()

                for neighbour in valve.neighbours:

                    # this assumes the first route was shorter?
                    if neighbour.label in visited:
                        continue

                    visited.add(neighbour.label)

                    # store distance if valve not blocked (compress graph)
                    if neighbour.flow_rate > 0:
                        distances[label][neighbour.label] = distance + 1

                    queue.append((distance + 1, neighbour))

        return distances


class Puzzle:
    def __init__(
        self, time_to_eruption: int, begin_valve: Valve, num_players: Optional[int] = 1
    ) -> None:
        self.time_to_eruption = time_to_eruption
        self.begin_valve = begin_valve
        self.num_players = num_players
        # keep track of combinations of open valves
        self.cache = {}

    def solve(self) -> int:
        state = ValvesState()
        total_released_pressure = 0
        for _ in range(self.num_players):
            print("begin", id(state))
            # released_pressure, state = self.depth_first_search(
            # time=0,
            released_pressure = self.depth_first_search(
                time_remaining=self.time_to_eruption,
                valve=self.begin_valve,
                state=state,
            )
            print("end", id(state))
            total_released_pressure += released_pressure

        return released_pressure

    def depth_first_search(
        self, time_remaining: int, valve: Valve, state: ValvesState
    ) -> int:

        # we have already made the calculation for this combination of input arguments
        if (time_remaining, valve.label, state.key) in self.cache:
            return self.cache[time_remaining, valve.label, state.key]

        if time_remaining == 0:
            return 0

        # total_pressure_release = max(
        #     self.depth_first_search(time_remaining - 1, tunnel.valve, state)
        #     for tunnel in valve.tunnels
        # )

        total_pressures_released = []

        for tunnel in valve.tunnels:
            total_pressures_released.append(
                self.depth_first_search(time_remaining - 1, tunnel.valve, state)
            )

        total_pressure_release = max(total_pressures_released)

        if valve.flow_rate > 0 and not state.is_valve_open(valve):

            new_valve_state = ValvesState.from_state(state)
            new_valve_state.open_valve(valve)

            total_pressure_release = max(
                total_pressure_release,
                (time_remaining - 1) * valve.flow_rate
                + self.depth_first_search(time_remaining - 1, valve, new_valve_state),
            )

        self.cache[time_remaining, valve.label, state.key] = total_pressure_release

        return total_pressure_release

    def depth_first_search2(self, time: int, valve: Valve, state: ValvesState) -> int:

        # depth first search
        # print(state.key)

        # we have already made the calculation for this combination of input arguments
        if (time, valve.label, state.key) in self.cache:
            return self.cache[time, valve.label, state.key], state

        total_pressure_release = 0

        new_total_pressures_released = []
        new_states = []

        # loop over tunnels where this valve leads to
        for tunnel in valve.tunnels:

            # We have already performed the calculation with this valve open
            if state.is_valve_open(tunnel.valve):
                continue

            new_time = time + tunnel.distance + 1

            # we can't reach this valve or opening it has no effect since the remaining time is 0
            if new_time >= self.time_to_eruption:
                continue

            added_pressure_release = tunnel.valve.flow_rate * (
                self.time_to_eruption - new_time
            )

            new_valve_state = ValvesState.from_state(state)
            new_valve_state.open_valve(tunnel.valve)

            new_total_pressure_released, new_state = self.depth_first_search(
                new_time, tunnel.valve, new_valve_state
            )

            new_total_pressures_released.append(
                new_total_pressure_released + added_pressure_release
            )
            new_states.append(new_state)

            # new_total_pressure_released += added_pressure_release

            # if new_total_pressure_released > total_pressure_release:
            #     total_pressure_release = new_total_pressure_released
            #     state = new_state

            # total_pressure_release = max(
            #     total_pressure_release,
            #     self.depth_first_search(new_time, tunnel.valve, new_valve_state)[0]
            #     + added_pressure_release,
            # )

        if len(new_total_pressures_released) > 0:

            max_total_pressure_release = max(new_total_pressures_released)

            if max_total_pressure_release > total_pressure_release:
                total_pressure_release = max_total_pressure_release

                index = new_total_pressures_released.index(max_total_pressure_release)

                new_state = new_states[index]
        else:
            new_state = state

        self.cache[time, valve.label, state.key] = total_pressure_release

        return total_pressure_release, new_state


def solve_part_one(lines: list[str], example: bool):
    valves = PuzzleInputParser.parse(lines)

    puzzle = Puzzle(time_to_eruption=30, begin_valve=valves["AA"], num_players=1)

    return puzzle.solve()


def solve_part_two(lines: list[str], example: bool):
    valves = PuzzleInputParser.parse(lines)

    puzzle = Puzzle(time_to_eruption=26, begin_valve=valves["AA"], num_players=2)

    return puzzle.solve()
