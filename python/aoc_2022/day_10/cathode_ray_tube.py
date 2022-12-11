from dataclasses import dataclass
from typing import Optional

from aoc_2022.utils import utils


class Memory:

    def __init__(self, instructions) -> None:
        self.instructions = [i for i in reversed(instructions)]


@dataclass
class Instruction:
    command: str
    arg: Optional[int] = None


class CPU:

    def __init__(self, memory) -> None:
        self.memory = memory
        self.x = 1
        self.state = "idle"
        self.instruction = None
        self.cycle = 1
        self.signal_strength = {}
        self.total_signal_strength = 0

    def tick(self):

        if (self.cycle - 20) % 40 == 0:
            signal_strength = self.cycle * self.x
            print(f"cycle = {self.cycle}, X = {self.x}, signal_strength: {signal_strength}")
            self.signal_strength[self.cycle] = signal_strength
            self.total_signal_strength += signal_strength

        # if state is idle get new instruction
        if self.state == "idle":
            try:
                self.instruction = self.memory.instructions.pop()
                if self.instruction.command == "addx":
                    self.state = "addx"
            except IndexError:
                self.state = "done"
        elif self.state == "addx":
            self.x += self.instruction.arg
            self.state = "idle"

        self.cycle += 1

class Clock:

    def __init__(self, cpu) -> None:
        self.cpu = cpu

    def run(self):
        while True:
            self.cpu.tick()
            if self.cpu.state == "done":
                break



def parse_instructions(lines):
    instructions = []
    for line in lines:
        parts = line.split()
        command = parts[0]
        if len(parts) == 1:
            instructions.append(Instruction(command))
            continue
        arg = int(parts[1])
        instructions.append(Instruction(command, arg))

    return instructions




def solve_part_one(lines):
    instructions = parse_instructions(lines)

    memory = Memory(instructions)
    cpu = CPU(memory=memory)
    clock = Clock(cpu=cpu)

    clock.run()

    return cpu.total_signal_strength




def solve_part_two(lines):
    pass


def main():

    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 10: Cathode-Ray Tube ---")
    answer_part_one = solve_part_one(lines)
    print(f"Answer part one: {answer_part_one}")

    print("--- Part Two ---")
    answer_part_two = solve_part_two(lines)
    print(f"Answer part two: {answer_part_two}")


if __name__ == "__main__":
    main()