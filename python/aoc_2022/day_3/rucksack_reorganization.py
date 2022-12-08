import string
import sys
from pathlib import Path


def split_rucksack_content_into_compartments(content: str):
    middle_index = len(content) // 2

    return content[:middle_index], content[middle_index:]


def find_items_in_both_compartments(first_compartment, second_compartment):
    items_in_both_compartments = []

    for item in first_compartment:

        if item not in second_compartment:
            continue

        # don't store duplicates
        if item not in items_in_both_compartments:
            items_in_both_compartments.append(item)

    return items_in_both_compartments


def find_badge_of_group(rucksacks):
    intersection = set.intersection(
        set(rucksacks[0]), set(rucksacks[1]), set(rucksacks[2])
    )
    return list(intersection)[0]


def get_item_priority(item: str):
    if item.islower():
        return string.ascii_lowercase.index(item) + 1

    if item.isupper():
        return string.ascii_uppercase.index(item) + 26 + 1

    raise ValueError(f"Item should be one [a-z|A-Z] character: '{item}'")


def part_one(lines):
    sum_of_priorities = 0

    for content in lines:
        (
            first_compartment,
            second_compartment,
        ) = split_rucksack_content_into_compartments(content)
        duplicate_item = find_items_in_both_compartments(
            first_compartment, second_compartment
        )[0]
        sum_of_priorities += get_item_priority(duplicate_item)

    print(f"Total priorities part 1: {sum_of_priorities}")


def part_two(lines):
    sum_of_priorities = 0

    for i in range(0, len(lines) + 1 - 3, 3):
        group_rucksacks = lines[i : i + 3]
        badge = find_badge_of_group(group_rucksacks)
        sum_of_priorities += get_item_priority(badge)

    print(f"Total priorities part 2: {sum_of_priorities}")


def main(input_file):
    input_file_path = Path(__file__).with_name(input_file)

    with open(input_file_path, "r") as fh:
        lines = [l for l in fh.read().splitlines()]

    part_one(lines)
    part_two(lines)


if __name__ == "__main__":
    input_file = "puzzle_input.txt"

    if len(sys.argv) >= 2 and sys.argv[1] == "example":
        print("Using example data")
        input_file = "puzzle_input_example.txt"

    main(input_file)
