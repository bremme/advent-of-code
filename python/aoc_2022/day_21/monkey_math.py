from ast import operator
from asyncio import wait_for
from dataclasses import dataclass
from typing import Optional


@dataclass
class Monkey:

    name: str
    number: Optional[int] = None
    wait_for_monkeys: Optional[tuple[str]] = None
    operator: Optional[str] = None


def parse(lines):

    monkeys = {}

    for line in lines:
        name, job = line.split(": ")

        if job.isnumeric():
            monkeys[name] = Monkey(name=name, number=int(job))
            continue
        other_monkeys = job[:4], job[7:]
        operator = job[5]
        monkeys[name] = Monkey(
            name=name, wait_for_monkeys=other_monkeys, operator=operator
        )

    return monkeys


def find_number_monkey_yells(name, monkeys: list[Monkey]):
    monkey = monkeys[name]

    if monkey.number is not None:
        return monkey.number

    name_one, name_two = monkey.wait_for_monkeys
    number_one = find_number_monkey_yells(name_one, monkeys=monkeys)
    number_two = find_number_monkey_yells(name_two, monkeys=monkeys)

    if monkey.operator == "+":
        return number_one + number_two

    if monkey.operator == "-":
        return number_one - number_two

    if monkey.operator == "/":
        return number_one // number_two

    if monkey.operator == "*":
        return number_one * number_two


def solve_part_one(lines, example):
    monkeys = parse(lines)

    return find_number_monkey_yells("root", monkeys)


def solve_part_two(lines, example):
    pass
