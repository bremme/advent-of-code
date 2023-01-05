from aoc.utils import utils


def parse_ranges(line: str) -> tuple[set, set]:
    range_numbers = [int(e) for e in line.replace("-", ",").split(",")]

    first_start, first_end = range_numbers[:2]
    second_start, second_end = range_numbers[2:]

    first_range = [section_id for section_id in range(first_start, first_end + 1)]
    second_range = [section_id for section_id in range(second_start, second_end + 1)]

    return set(first_range), set(second_range)


def solve_part_two(lines: list[str], example: bool) -> int:
    num_overlapping_pairs = 0

    for line in lines:
        first_range, second_range = parse_ranges(line)

        if first_range.intersection(second_range):
            num_overlapping_pairs += 1

    return num_overlapping_pairs


def solve_part_one(lines: list[str], example: bool) -> int:
    num_fully_contained_pairs = 0

    for line in lines:
        first_range, second_range = parse_ranges(line)

        if first_range.issubset(second_range) or second_range.issubset(first_range):
            num_fully_contained_pairs += 1

    return num_fully_contained_pairs


def main():
    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 4: Camp Cleanup ---")
    num_overlapping_pairs = solve_part_one(lines)
    print(f"Number overlapping pairs: {num_overlapping_pairs}")

    print("--- Part Two ---")
    num_fully_contained_pairs = solve_part_two(lines)
    print(f"Number fully contained pairs: {num_fully_contained_pairs}")


if __name__ == "__main__":
    main()
