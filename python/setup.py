from importlib.metadata import entry_points

from setuptools import find_packages, setup

setup(
    name="aoc_2022",
    version="0.1.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["aoc=aoc_2022.__main__:main"]},
)
