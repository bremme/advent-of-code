import sys
from pathlib import Path


def parse_stacks(lines):

    index = lines.index("")

    stacks_description = [x for x in reversed(lines[:index])]

    num_stacks = int(stacks_description[0].split()[-1])

    stacks = [[] for stack in range(num_stacks)]

    # parse lines which describe the stacks
    for line in stacks_description[1:]:
        # loop over stacks
        for stack_number in range(0, num_stacks):
            crate_index = (4 * stack_number) + 1

            # deal with removed white spaces (not required for original input)
            if crate_index >= len(line):
                break

            crate = line[crate_index]

            # no crate in this stack at this height
            if crate == " ":
                continue

            stacks[stack_number].append(crate)

    return stacks


def parse_procedure(lines):
    index = lines.index("")
    procedure_description = lines[index + 1 :]

    procedures = []

    for line in procedure_description:
        procedure = [
            int(number)
            for number in line.replace("move", "")
            .replace("from", "")
            .replace("to", "")
            .split()
        ]
        procedures.append(procedure)

    return procedures


def get_crates_on_top(stacks):
    return "".join([stack[-1] for stack in stacks])


def part_one(lines):
    stacks = parse_stacks(lines)

    procedures = parse_procedure(lines)

    for (num_to_move, from_stack, to_stack) in procedures:

        for _ in range(num_to_move):
            stacks[to_stack - 1].append(stacks[from_stack - 1].pop())

    top_crates = get_crates_on_top(stacks)
    print(top_crates)


def part_two(lines):
    stacks = parse_stacks(lines)

    procedures = parse_procedure(lines)

    for (num_to_move, from_stack, to_stack) in procedures:

        moved_crates = [stacks[from_stack - 1].pop() for _ in range(num_to_move)]
        moved_crates.reverse()

        stacks[to_stack - 1].extend(moved_crates)

    top_crates = get_crates_on_top(stacks)

    print(top_crates)


def main(input_file):
    input_file_path = Path(__file__).with_name(input_file)

    with open(input_file_path, "r") as fh:
        lines = [line for line in fh.read().splitlines()]

    part_one(lines)
    part_two(lines)


if __name__ == "__main__":
    input_file = "puzzle_input.txt"

    if len(sys.argv) >= 2 and sys.argv[1] == "example":
        print("Using example data")
        input_file = "puzzle_input_example.txt"

    main(input_file)
