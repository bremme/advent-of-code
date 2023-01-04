import string

from aoc.utils import utils


def split_rucksack_content_into_compartments(content: str):
    middle_index = len(content) // 2

    return content[:middle_index], content[middle_index:]


def find_items_in_both_compartments(first_compartment, second_compartment):
    items_in_both_compartments = []

    for item in first_compartment:

        if item not in second_compartment:
            continue

        # don't store duplicates
        if item in items_in_both_compartments:
            continue

        items_in_both_compartments.append(item)

    return items_in_both_compartments


def find_badge_of_group(rucksacks):
    # item that is found in all three rucksacks is the group badge
    intersection = set.intersection(
        set(rucksacks[0]), set(rucksacks[1]), set(rucksacks[2])
    )
    return list(intersection)[0]


def get_item_priority(item: str):
    # a through z have priority 1 through 26
    if item.islower():
        return string.ascii_lowercase.index(item) + 1

    # A through Z have priority 27 through 52
    if item.isupper():
        return string.ascii_uppercase.index(item) + 26 + 1

    raise ValueError(f"Item should be one [a-z|A-Z] character: '{item}'")


def solve_part_one(lines, example=False):
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

    return sum_of_priorities


def solve_part_two(lines):
    NUM_ELVES_IN_GROUP = 3
    sum_of_priorities = 0

    for i in range(0, len(lines) + 1 - NUM_ELVES_IN_GROUP, NUM_ELVES_IN_GROUP):
        group_rucksacks = lines[i : i + NUM_ELVES_IN_GROUP]
        badge = find_badge_of_group(group_rucksacks)
        sum_of_priorities += get_item_priority(badge)

    return sum_of_priorities


def main():
    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 3: Rucksack Reorganization ---")
    sum_of_priorities_part_one = solve_part_one(lines)
    print(f"Total priorities: {sum_of_priorities_part_one}")

    print("--- Part Two ---")
    sum_of_priorities_part_two = solve_part_two(lines)
    print(f"Total priorities: {sum_of_priorities_part_two}")


if __name__ == "__main__":
    main()
