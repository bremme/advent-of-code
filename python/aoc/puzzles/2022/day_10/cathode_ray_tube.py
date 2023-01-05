from dataclasses import dataclass
from enum import Enum
from typing import Optional

from aoc.utils import utils


@dataclass
class Instruction:
    command: str
    arg: Optional[int] = None


class Memory:
    def __init__(self, instructions: list[Instruction]) -> None:
        self.instructions = [i for i in reversed(instructions)]


class CPU:
    def __init__(self, memory: Memory) -> None:
        self.memory = memory
        self.x = 1
        self.state = "idle"
        self.instruction = None
        self.cycle = 1
        self.signal_strength = {}
        self.total_signal_strength = 0

    def tick(self):

        # every 40th cycle starting at 20
        if (self.cycle - 20) % 40 == 0:
            signal_strength = self.cycle * self.x
            # print(f"cycle = {self.cycle}, X = {self.x}, signal_strength: {signal_strength}")
            self.signal_strength[self.cycle] = signal_strength
            self.total_signal_strength += signal_strength

        # if state is idle get new instruction
        if self.state == "idle":

            self.instruction = self.memory.instructions.pop()

            if self.instruction.command == "addx":
                self.state = "addx"

        # else if we started an addx instruction, finish it
        elif self.state == "addx":
            self.x += self.instruction.arg
            self.state = "idle"

        if len(self.memory.instructions) == 0:
            self.state = "done"

        self.cycle += 1


class Clock:
    def __init__(self, cpu, crt=None) -> None:
        self.cpu = cpu
        self.crt = crt

    def run(self):
        while True:
            if self.crt:
                self.crt.tick()

            self.cpu.tick()

            if self.cpu.state == "done":
                break


class Pixel(Enum):
    DARK = "."
    LIT = "#"
    DARK_BLACK_CIRCLE = "⚫"
    LIT_WHITE_CIRCLE = "⚪"


class CRT:
    def __init__(
        self, width, height, cpu, dark_pixel=Pixel.DARK, lit_pixel=Pixel.LIT
    ) -> None:
        self.width = width
        self.height = height
        self.cpu = cpu
        self.dark_pixel = dark_pixel
        self.lit_pixel = lit_pixel
        self.row = 0
        self.col = 0
        self.frame_buffer = [[dark_pixel] * self.width for _ in range(self.height)]

    def tick(self):

        pixel = self._get_pixel()

        self.frame_buffer[self.row][self.col] = pixel.value

        self.col += 1

        if self.col == self.width:
            self.col = 0
            self.row += 1

    def _get_pixel(self):
        sprite_column = self.cpu.x

        if self.col in [sprite_column - 1, sprite_column, sprite_column + 1]:
            return self.lit_pixel

        return self.dark_pixel

    def display(self):
        for row in range(self.height):
            print("".join(self.frame_buffer[row]))

    def __str__(self):
        display_str = []
        for row in range(self.height):
            display_str.append("".join(self.frame_buffer[row]))
        return "\n\n" + "\n".join(display_str) + "\n"


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


def solve_part_one(lines: list[str], example: bool) -> int:
    instructions = parse_instructions(lines)

    memory = Memory(instructions=instructions)
    cpu = CPU(memory=memory)
    clock = Clock(cpu=cpu)

    clock.run()

    return cpu.total_signal_strength


def solve_part_two(lines: list[str], example: bool) -> int:
    instructions = parse_instructions(lines)
    memory = Memory(instructions=instructions)
    cpu = CPU(memory=memory)
    crt = CRT(
        width=40,
        height=6,
        cpu=cpu,
        dark_pixel=Pixel.DARK_BLACK_CIRCLE,
        lit_pixel=Pixel.LIT_WHITE_CIRCLE,
    )
    clock = Clock(cpu=cpu, crt=crt)

    clock.run()

    return crt


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
