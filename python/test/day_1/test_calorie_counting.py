import unittest

from aoc_2022.day_1.calorie_counting import (
    parse_how_many_calories_are_carried_by_each_elf,
    solve_part_one,
    solve_part_two,
)
from aoc_2022.utils import utils


class TestCalorieCounting(unittest.TestCase):
    def test_solve_part_one_example(self):
        lines = utils.read_puzzle_input(day=1, example=True)
        elf_calories = parse_how_many_calories_are_carried_by_each_elf(lines)
        highest_calories = solve_part_one(elf_calories)

        self.assertEqual(highest_calories, 24000)

    def test_solve_part_one(self):
        lines = utils.read_puzzle_input(day=1, example=False)
        elf_calories = parse_how_many_calories_are_carried_by_each_elf(lines)
        highest_calories = solve_part_one(elf_calories)

        self.assertEqual(highest_calories, 69177)

    def test_solve_part_two_example(self):
        lines = utils.read_puzzle_input(day=1, example=True)
        elf_calories = parse_how_many_calories_are_carried_by_each_elf(lines)
        total_calories_top_three = solve_part_two(elf_calories)

        self.assertEqual(total_calories_top_three, 45000)

    def test_solve_part_two(self):
        lines = utils.read_puzzle_input(day=1, example=False)
        elf_calories = parse_how_many_calories_are_carried_by_each_elf(lines)
        total_calories_top_three = solve_part_two(elf_calories)

        self.assertEqual(total_calories_top_three, 207456)


if __name__ == "__main__":
    unittest.main()
