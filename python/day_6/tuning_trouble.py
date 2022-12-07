import sys
from pathlib import Path


def find_marker_index(buffer, num_chars):
    for i in range(0, len(buffer) - num_chars):
        window = buffer[i : i + num_chars]

        # if all characters are unique, we found the marker
        if len(set(window)) == len(window):
            return i + num_chars


def part_one(lines):
    start_packet_distinct_chars = 4
    for line in lines:
        print(find_marker_index(line, start_packet_distinct_chars))


def part_two(lines):
    start_message_marker_distinct_chars = 14
    for line in lines:
        print(find_marker_index(line, start_message_marker_distinct_chars))


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
