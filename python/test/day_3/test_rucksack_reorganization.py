import unittest

from aoc_2022.day_3.rucksack_reorganization import (
    find_items_in_both_compartments,
    get_item_priority,
    solve_part_one,
    solve_part_two,
    split_rucksack_content_into_compartments,
)
from aoc_2022.utils import utils

DAY = 3
YEAR = 2022


class TestRuckSackReorganization(unittest.TestCase):
    def test_split_rucksack_content_into_compartments(self):
        expected_compartments = [
            ("vJrwpWtwJgWrhcsFMMfFFhFp", "vJrwpWtwJgWr", "hcsFMMfFFhFp"),
            ("PmmdzqPrVvPwwTWBwg", "PmmdzqPrV", "vPwwTWBwg"),
        ]

        for expectation in expected_compartments:
            content = expectation[0]
            expected_first_compartment = expectation[1]
            expected_second_compartment = expectation[2]
            (
                first_compartment,
                second_compartment,
            ) = split_rucksack_content_into_compartments(content)
            self.assertEqual(expected_first_compartment, first_compartment)
            self.assertEqual(expected_second_compartment, second_compartment)

    def test_find_items_in_both_compartments(self):
        expected_items_in_both_compartments = (
            ("vJrwpWtwJgWr", "hcsFMMfFFhFp", ["p"]),
            ("jqHRNqRjqzjGDLGL", "rsFMfFZSrLrFZsSL", ["L"]),
        )

        for (
            first_compartment,
            second_compartment,
            expected_items,
        ) in expected_items_in_both_compartments:
            items = find_items_in_both_compartments(
                first_compartment, second_compartment
            )
            self.assertListEqual(expected_items, items)

    def test_get_item_priority(self):
        expected_priorities = {"p": 16, "L": 38, "P": 42, "v": 22, "t": 20, "s": 19}

        for item, expected_priority in expected_priorities.items():
            priority = get_item_priority(item)
            self.assertEqual(expected_priority, priority)

    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

        answer = solve_part_one(lines)

        self.assertEqual(answer, 157)

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

        answer = solve_part_one(lines)

        self.assertEqual(answer, 8515)

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

        answer = solve_part_two(lines)

        self.assertEqual(answer, 70)

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

        answer = solve_part_two(lines)

        self.assertEqual(answer, 2434)


if __name__ == "__main__":
    unittest.main()
