import unittest

from aoc.day_11.monkey_in_the_middle import solve_part_one, solve_part_two
from aoc.utils import utils

DAY = 11
YEAR = 2022

EXPECTED_ANSWER_PART_ONE_EXAMPLE = 10605
EXPECTED_ANSWER_PART_ONE = 120384
EXPECTED_ANSWER_PART_TWO_EXAMPLE = 2713310158
EXPECTED_ANSWER_PART_TWO = 32059801242


class TestMonkeyInTheMiddle(unittest.TestCase):
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
