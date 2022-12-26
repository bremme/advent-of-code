import importlib
from dataclasses import dataclass
from operator import mod
from pathlib import Path
from types import ModuleType


@dataclass(frozen=True)
class PuzzleSolutionVariant:
    name: str
    module: ModuleType


@dataclass(frozen=True)
class Puzzle:
    title: str
    day: int
    solutions: list[PuzzleSolutionVariant]

    def get_solution(self, name):
        # support kebab-case and snake_case variant names
        name = name.replace("-", "_")
        for solution in self.solutions:
            if solution.name == name:
                return solution
        raise ValueError(f"No module defined for this variant '{name}'")


@dataclass(frozen=True)
class PuzzleCollection:
    puzzles: list[Puzzle]

    def get_puzzle(self, day: int):

        for puzzle in self.puzzles:
            if puzzle.day == day:
                return puzzle
        raise ValueError(f"No puzzle defined for day {day}")


class PuzzleFinder:
    @staticmethod
    def find_puzzles(root_path: Path) -> PuzzleCollection:
        NUM_ADVENT_DAYS = 25

        puzzles = []

        for day in range(1, NUM_ADVENT_DAYS + 1):

            module_dir = root_path / f"day_{day}"

            if not module_dir.exists():
                continue

            module_names = PuzzleFinder.find_module_names(module_dir)

            if len(module_names) == 0:
                continue

            default_module_name = PuzzleFinder.remove_default_module_name(module_names)

            default_module = PuzzleFinder.load_module(default_module_name, day=day)

            title = default_module_name.replace("_", " ").title()

            solutions = [PuzzleSolutionVariant(name="default", module=default_module)]

            for module_name in module_names:
                name = module_name.split(f"{default_module_name}_")[-1]
                module = PuzzleFinder.load_module(module_name, day=day)
                solutions.append(PuzzleSolutionVariant(name=name, module=module))

            puzzles.append(Puzzle(day=day, title=title, solutions=solutions))

        return PuzzleCollection(puzzles)

    @staticmethod
    def find_module_names(module_dir: Path):
        module_names = []

        for path in module_dir.iterdir():
            if path.is_dir():
                continue
            if path.name.startswith("__"):
                continue
            if path.name.split(".")[-1] != "py":
                continue
            module_names.append("".join(path.name.split(".")[:-1]))

        return module_names

    @staticmethod
    def remove_default_module_name(module_names: list[str]):
        # assume the file/module with the shortest name is the default
        return module_names.pop(module_names.index(min(module_names, key=len)))

    @staticmethod
    def load_module(module_name: str, day: int):
        return importlib.import_module(f"aoc_2022.day_{day}.{module_name}")
