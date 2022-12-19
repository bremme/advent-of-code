import unittest

from aoc_2022.day_14.regolith_reservoir_naive import solve_part_one, solve_part_two
from aoc_2022.utils import utils

DAY = 14

EXPECTED_ANSWER_PART_ONE_EXAMPLE = 24
EXPECTED_ANSWER_PART_ONE = 913
EXPECTED_ANSWER_PART_TWO_EXAMPLE = 93
EXPECTED_ANSWER_PART_TWO = 30762


class TestRegolithReservoir(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=DAY, example=True)

        answer = solve_part_one(lines)

        self.assertEqual(answer, EXPECTED_ANSWER_PART_ONE_EXAMPLE)

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=DAY, example=False)

        answer = solve_part_one(lines)

        self.assertEqual(answer, EXPECTED_ANSWER_PART_ONE)

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=DAY, example=True)

        answer = solve_part_two(lines)

        self.assertEqual(answer, EXPECTED_ANSWER_PART_TWO_EXAMPLE)

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=DAY, example=False)

        answer = solve_part_two(lines)

        self.assertEqual(answer, EXPECTED_ANSWER_PART_TWO)


if __name__ == "__main__":
    unittest.main()
