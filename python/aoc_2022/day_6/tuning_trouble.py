from aoc_2022.utils import utils


def find_markers(lines, num_chars):
    marker_indices = []
    for line in lines:
        marker_indices.append(find_marker(line, num_chars))

    return marker_indices[0] if len(marker_indices) == 1 else marker_indices

def find_marker(buffer, num_chars):
    for i in range(0, len(buffer) - num_chars):
        window = buffer[i : i + num_chars]

        # if all characters are unique, we found the marker
        if len(set(window)) == len(window):
            return i + num_chars


def solve_part_one(lines):
    start_message_marker_distinct_chars = 4
    return find_markers(lines, num_chars=start_message_marker_distinct_chars)


def solve_part_two(lines):
    start_message_marker_distinct_chars = 14
    return find_markers(lines, num_chars=start_message_marker_distinct_chars)


def main():
    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 6: Tuning Trouble ---")
    answer_part_one = solve_part_one(lines)
    print(f"Answer part one: {answer_part_one}")

    print("--- Part Two ---")
    answer_part_two = solve_part_two(lines)
    print(f"Answer part two: {answer_part_two}")


if __name__ == "__main__":
    main()
