import unittest

from aoc.day_2.rock_paper_scissors import solve_part_one, solve_part_two
from aoc.utils import utils

DAY = 2
YEAR = 2022


class TestCalorieCounting(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

        total_score = solve_part_one(lines)

        self.assertEqual(total_score, 15)

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

        total_score = solve_part_one(lines)

        self.assertEqual(total_score, 10718)

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=True)

        total_score = solve_part_two(lines)

        self.assertEqual(total_score, 12)

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=DAY, year=YEAR, example=False)

        total_score = solve_part_two(lines)

        self.assertEqual(total_score, 14652)


if __name__ == "__main__":
    unittest.main()
