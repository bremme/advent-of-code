from dataclasses import dataclass
from typing import Optional


@dataclass
class Monkey:

    name: str
    number: Optional[int] = None
    waiting_for_monkeys: Optional[tuple[str]] = None
    operator: Optional[str] = None


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def divide(a, b):
    return a // b


def multiply(a, b):
    return a * b


operations = {
    "+": add,
    "-": subtract,
    "/": divide,
    "*": multiply,
}


def perform_operation(operation, a, b):
    return operations[operation](a, b)


def parse(lines) -> dict[str, Monkey]:

    monkeys = {}

    for line in lines:
        name, job = line.split(": ")

        if job.isnumeric():
            monkeys[name] = Monkey(name=name, number=int(job))
            continue
        other_monkeys = job[:4], job[7:]
        operator = job[5]
        monkeys[name] = Monkey(
            name=name, waiting_for_monkeys=other_monkeys, operator=operator
        )

    return monkeys


def find_number_monkey_yells(monkey, monkeys: list[Monkey]):

    if monkey.number is not None:
        return monkey.number

    name_one, name_two = monkey.waiting_for_monkeys

    number_one = find_number_monkey_yells(monkeys[name_one], monkeys=monkeys)
    number_two = find_number_monkey_yells(monkeys[name_two], monkeys=monkeys)

    return perform_operation(monkey.operator, number_one, number_two)

    if monkey.operator == "+":
        return number_one + number_two

    if monkey.operator == "-":
        return number_one - number_two

    if monkey.operator == "/":
        return number_one // number_two

    if monkey.operator == "*":
        return number_one * number_two


def is_monkey_waiting_for_other_monkey(monkey: Monkey, other_monkey: Monkey, monkeys):
    # if this monkey is waiting for other monkey, its in the same tree

    if monkey.waiting_for_monkeys is None:
        return False

    if other_monkey.name in monkey.waiting_for_monkeys:
        return True

    for monkey_to_wait_for_name in monkey.waiting_for_monkeys:
        # if in any of these tree a monkey is waiting for other monkey return True
        if is_monkey_waiting_for_other_monkey(
            monkeys[monkey_to_wait_for_name], other_monkey, monkeys
        ):
            return True

    return False


def solve_part_one(lines, example):
    monkeys = parse(lines)

    return find_number_monkey_yells(monkeys["root"], monkeys)


def solve_part_two(lines, example):
    monkeys = parse(lines)

    you = monkeys["humn"]

    # find out in with tree I (humn) belong
    root_monkey = monkeys["root"]
    left_monkey_name, right_monkey_name = root_monkey.waiting_for_monkeys

    left_monkey = monkeys[left_monkey_name]
    right_monkey = monkeys[right_monkey_name]

    part_of_left = is_monkey_waiting_for_other_monkey(left_monkey, you, monkeys)

    if part_of_left:
        number_to_match = find_number_monkey_yells(right_monkey, monkeys)
        last_monkey = left_monkey
    else:
        number_to_match = find_number_monkey_yells(left_monkey, monkeys)
        last_monkey = right_monkey

    # find number from other tree

    # find number to yell
    # choose a number
    # move up the tree
    # if number too high break
    # increase number
    # if end and number too low
    # decrease number

    # find number to yell

    guess = number_to_match

    while True:
        you.number = guess

        number = find_number_monkey_yells(last_monkey, monkeys)

        breakpoint()

        print(f"guess {guess} -> number {number}")

        if number > number_to_match:
            factor = (number - number_to_match) / 100
            guess -= 1
        else:
            guess += 1

        if number == number_to_match:
            break

    return guess
