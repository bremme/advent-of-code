from importlib.metadata import entry_points

from setuptools import find_packages, setup

setup(
    name="aoc",
    version="0.1.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["aoc=aoc.__main__:main"]},
)
