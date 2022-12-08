import unittest

from aoc_2022.day_5.supply_stacks import solve_part_one, solve_part_two
from aoc_2022.utils import utils

DAY = 5


class TestCleanUp(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=DAY, example=True)

        answer = solve_part_one(lines)

        self.assertEqual(answer, "CMZ")

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=DAY, example=False)

        answer = solve_part_one(lines)

        self.assertEqual(answer, "SHQWSRBDL")

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=DAY, example=True)

        answer = solve_part_two(lines)

        self.assertEqual(answer, "MCD")

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=DAY, example=False)

        answer = solve_part_two(lines)

        self.assertEqual(answer, "CDTQZHBRS")
