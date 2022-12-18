import unittest

from aoc_2022.day_2.rock_paper_scissors import solve_part_one, solve_part_two
from aoc_2022.utils import utils


class TestCalorieCounting(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=2, example=True)

        total_score = solve_part_one(lines)

        self.assertEqual(total_score, 15)

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=2, example=False)

        total_score = solve_part_one(lines)

        self.assertEqual(total_score, 10718)

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=2, example=True)

        total_score = solve_part_two(lines)

        self.assertEqual(total_score, 12)

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=2, example=False)

        total_score = solve_part_two(lines)

        self.assertEqual(total_score, 14652)


if __name__ == "__main__":
    unittest.main()
