from dataclasses import dataclass
from typing import Optional

from numpy import gradient


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
    return a / b


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


def find_number_monkey_yells(monkey, monkeys: list[Monkey]) -> float:

    if monkey.number is not None:
        return monkey.number

    name_one, name_two = monkey.waiting_for_monkeys

    number_one = find_number_monkey_yells(monkeys[name_one], monkeys=monkeys)
    number_two = find_number_monkey_yells(monkeys[name_two], monkeys=monkeys)

    return perform_operation(monkey.operator, number_one, number_two)


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


def use_binairy_search_to_find_what_monkey_needs_to_yell(
    monkey, monkey_to_match, number_to_match, monkeys
):
    low = -1e20
    high = 1e20
    guess = monkey.number
    iterations = 0
    max_iterations = 1e6

    # find gradient
    monkey.number = low
    low_number = find_number_monkey_yells(monkey_to_match, monkeys)

    monkey.number = high
    high_number = find_number_monkey_yells(monkey_to_match, monkeys)

    if high_number > low_number:
        positive_gradient = True
    else:
        positive_gradient = False

    while iterations < max_iterations:
        monkey.number = guess

        number = find_number_monkey_yells(monkey_to_match, monkeys)

        if number == number_to_match:
            return monkey.number

        # determine new guess
        if positive_gradient:
            if number > number_to_match:
                high = guess
            else:
                low = guess
        else:
            if number > number_to_match:
                low = guess
            else:
                high = guess

        guess = (high + low) // 2

        iterations += 1

    raise RuntimeError("Max iterations reached")


def solve_part_one(lines, example):
    monkeys = parse(lines)

    return int(find_number_monkey_yells(monkeys["root"], monkeys))


def solve_part_two(lines, example):
    monkeys = parse(lines)

    you = monkeys["humn"]

    # find out in with tree I (humn) belong
    root_monkey = monkeys["root"]
    left_monkey_name, right_monkey_name = root_monkey.waiting_for_monkeys

    left_monkey = monkeys[left_monkey_name]
    right_monkey = monkeys[right_monkey_name]

    humn_is_part_of_left = is_monkey_waiting_for_other_monkey(left_monkey, you, monkeys)

    if humn_is_part_of_left:
        number_to_match = find_number_monkey_yells(right_monkey, monkeys)
        new_root_monkey = left_monkey
    else:
        number_to_match = find_number_monkey_yells(left_monkey, monkeys)
        new_root_monkey = right_monkey

    return int(
        use_binairy_search_to_find_what_monkey_needs_to_yell(
            monkey=you,
            monkey_to_match=new_root_monkey,
            number_to_match=number_to_match,
            monkeys=monkeys,
        )
    )
