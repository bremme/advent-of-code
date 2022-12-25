
from dataclasses import dataclass
import re
from typing import Optional
from aoc_2022.utils.utils import parse_positive_integers


@dataclass
class Valve:
    label: str
    flow_rate: int
    open: Optional[bool] = False
    neighbours: Optional[list["Valve"]] = None



def parse(lines: list[str]) -> dict[str, Valve]:
    neighbours = {}
    valves = {}

    for line in lines:
        labels = re.findall("[A-Z][A-Z]+", line)
        flow_rate = parse_positive_integers(line)[0]

        valve = Valve(label=labels[0], flow_rate=flow_rate)

        neighbours[labels[0]] = labels[1:]

        valves[labels[0]] = valve

    for valve_label, neighbours_labels in neighbours.items():
        valves[valve_label].neighbours = [valves[label] for label in neighbours_labels]

    return valves


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
                print(f"Valve {self.open_valves[0].label} is open, releasing {self.release_pressure_per_minute} pressure.")
            else:
                valve_labels = ", ".join([valve.label for valve in self.open_valves])
                print(f"Valves {valve_labels} are open, releasing {self.release_pressure_per_minute} pressure.")


            self.__release_pressure()

            # valve is closed and flow rate > 0
            if self.valve.open is False and self.valve.flow_rate > 0:
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

    valve = valves["AA"]

    puzzle = Puzzle(minutes_left=30, valve=valve)

    puzzle.solve()

    return puzzle.total_released_pressure







def solve_part_two(lines: list[str], example: bool):
    pass