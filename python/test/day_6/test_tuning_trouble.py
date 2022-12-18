import unittest

from aoc_2022.day_6.tuning_trouble import solve_part_one, solve_part_two
from aoc_2022.utils import utils

DAY = 6


class TestTuningTrouble(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=DAY, example=True)

        answer = solve_part_one(lines)

        self.assertEqual(answer, [7, 5, 6, 10, 11])

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=DAY, example=False)

        answer = solve_part_one(lines)

        self.assertEqual(answer, 1262)

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=DAY, example=True)

        answer = solve_part_two(lines)

        self.assertEqual(answer, [19, 23, 23, 29, 26])

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=DAY, example=False)

        answer = solve_part_two(lines)

        self.assertEqual(answer, 3444)


if __name__ == "__main__":
    unittest.main()
