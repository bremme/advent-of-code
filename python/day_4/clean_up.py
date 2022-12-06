import sys
from pathlib import Path


def parse_ranges(line: str) -> tuple[set]:
    range_numbers = [int(e) for e in line.replace("-", ",").split(",")]

    first_start, first_end = range_numbers[:2]
    second_start, second_end = range_numbers[2:]

    first_range = [section_id for section_id in range(first_start, first_end + 1)]
    second_range = [section_id for section_id in range(second_start, second_end + 1)]

    return set(first_range), set(second_range)


def part_two(lines: list[str]) -> None:
    num_overlapping_pairs = 0

    for line in lines:
        first_range, second_range = parse_ranges(line)

        if first_range.intersection(second_range):
            num_overlapping_pairs += 1

    print(f"Number overlapping pairs: {num_overlapping_pairs}")


def part_one(lines: list[str]) -> None:
    num_fully_contained_pairs = 0

    for line in lines:
        first_range, second_range = parse_ranges(line)

        if first_range.issubset(second_range) or second_range.issubset(first_range):
            num_fully_contained_pairs += 1

    print(f"Number fully contained pairs: {num_fully_contained_pairs}")


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

# 485 it too high
