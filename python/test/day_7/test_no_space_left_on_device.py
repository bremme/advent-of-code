import unittest

from aoc_2022.day_7.no_space_left_on_device import solve_part_one, solve_part_two
from aoc_2022.utils import utils

DAY = 7

EXPECTED_ANSWER_PART_ONE_EXAMPLE = 95437
EXPECTED_ANSWER_PART_ONE = 1232307
EXPECTED_ANSWER_PART_TWO_EXAMPLE = 24933642
EXPECTED_ANSWER_PART_TWO = 7268994


class TestNoSpaceLeftOnDevice(unittest.TestCase):
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
