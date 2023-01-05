from aoc.utils import utils


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


def parse_procedures(lines):
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


def solve_part_one(lines: list[str], example: bool) -> int:
    stacks = parse_stacks(lines)

    procedures = parse_procedures(lines)

    for (num_to_move, from_stack, to_stack) in procedures:

        for _ in range(num_to_move):
            stacks[to_stack - 1].append(stacks[from_stack - 1].pop())

    crates_on_top = get_crates_on_top(stacks)

    return crates_on_top


def solve_part_two(lines: list[str], example: bool) -> int:
    stacks = parse_stacks(lines)

    procedures = parse_procedures(lines)

    for (num_to_move, from_stack, to_stack) in procedures:

        moved_crates = [stacks[from_stack - 1].pop() for _ in range(num_to_move)]
        moved_crates.reverse()

        stacks[to_stack - 1].extend(moved_crates)

    crates_on_top = get_crates_on_top(stacks)

    return crates_on_top


def main(input_file):
    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 4: Camp Cleanup ---")
    crates_on_top_part_one = solve_part_one(lines)
    print(f"Crates on top: {crates_on_top_part_one}")

    print("--- Part Two ---")
    crates_on_top_part_two = solve_part_two(lines)
    print(f"Crates on top: {crates_on_top_part_two}")


if __name__ == "__main__":
    main()
