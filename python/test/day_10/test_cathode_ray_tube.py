import unittest

from aoc_2022.day_10.cathode_ray_tube import solve_part_one
from aoc_2022.utils import utils

DAY = 10


class TestRopeBridge(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=DAY, example=True)

        answer = solve_part_one(lines)

        self.assertEqual(answer, 13140)

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=DAY, example=False)

        answer = solve_part_one(lines)

        self.assertEqual(answer, 14420)

