from aoc_2022.utils import utils


def parse_how_many_calories_are_carried_by_each_elf(lines) -> list[int]:
    elf_index = 0
    elf_calories = [0]
    elf_separator = ""

    for line in lines:
        # found new elf
        if line == elf_separator:
            elf_calories.append(0)
            elf_index += 1
            continue

        calories = int(line)
        elf_calories[elf_index] += calories

    return elf_calories


def find_elf_carrying_the_most_calories(elf_calories: list[int]) -> tuple[int]:
    calories = max(elf_calories)
    elf_with_highest_calories = elf_calories.index(calories)
    return calories, elf_with_highest_calories


def solve_part_one(lines: list[str], example: bool) -> int:

    elf_calories = parse_how_many_calories_are_carried_by_each_elf(lines)

    num_elves = len(elf_calories)
    highest_calories, carried_by_elf = find_elf_carrying_the_most_calories(elf_calories)

    # print(f"Number of elves: {num_elves}")
    # print(f"Carried by elf: {carried_by_elf}")

    return highest_calories


def solve_part_two(lines: list[str], example: bool) -> int:

    elf_calories = parse_how_many_calories_are_carried_by_each_elf(lines)

    highest_calories_top_three = sorted(elf_calories, reverse=True)[0:3]
    total_calories_top_three = sum(highest_calories_top_three)

    return total_calories_top_three


def main():

    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 1: Calorie Counting ---")
    highest_calories = solve_part_one(elf_calories)
    print(f"Highest number of calories: {highest_calories}")

    print("--- Part Two ---")
    total_calories_top_three = solve_part_two(elf_calories)
    print(f"Total calories top three: {total_calories_top_three}")


if __name__ == "__main__":
    main()
