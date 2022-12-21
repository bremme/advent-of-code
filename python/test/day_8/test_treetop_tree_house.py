import unittest

from aoc_2022.day_8.treetop_tree_house import solve_part_one, solve_part_two
from aoc_2022.utils import utils

DAY = 8
YEAR = 2022

EXPECTED_ANSWER_PART_ONE_EXAMPLE = 21
EXPECTED_ANSWER_PART_ONE = 1669
EXPECTED_ANSWER_PART_TWO_EXAMPLE = 8
EXPECTED_ANSWER_PART_TWO = 331344


class TestTreeTopTreeHouse(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

        answer = solve_part_one(lines)

        self.assertEqual(answer, EXPECTED_ANSWER_PART_ONE_EXAMPLE)

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

        answer = solve_part_one(lines)

        self.assertEqual(answer, EXPECTED_ANSWER_PART_ONE)

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

        answer = solve_part_two(lines)

        self.assertEqual(answer, EXPECTED_ANSWER_PART_TWO_EXAMPLE)

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

        answer = solve_part_two(lines)

        self.assertEqual(answer, EXPECTED_ANSWER_PART_TWO)


if __name__ == "__main__":
    unittest.main()
