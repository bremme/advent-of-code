import unittest

from aoc_2022.day_11.monkey_in_the_middle import solve_part_one, solve_part_two
from aoc_2022.utils import utils

DAY = 11


class TestRopeBridge(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=DAY, example=True)

        answer = solve_part_one(lines)

        self.assertEqual(answer, 10605)

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=DAY, example=False)

        answer = solve_part_one(lines)

        self.assertEqual(answer, 120384)

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=DAY, example=True)

        answer = solve_part_two(lines)

        self.assertEqual(answer, 2713310158)

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=DAY, example=False)

        answer = solve_part_two(lines)

        self.assertEqual(answer, 32059801242)
