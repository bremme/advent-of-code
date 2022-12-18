import logging
from typing import Optional

from aoc_2022.utils import utils

logger = logging.getLogger()


class Operation:
    def __init__(self, operator, arg) -> None:
        self.operator = operator
        self.arg = arg

    def inspect(self, item: int) -> int:

        if self.arg == "old":
            arg = item
        else:
            arg = int(self.arg)

        match self.operator:
            case "*":
                item *= arg
            case "+":
                item += arg
            case "-":
                item -= arg
            case "/":
                item /= arg
            case _:
                raise ValueError("Unknown operator")

        return item


class Test:
    def __init__(self, divisible_by, true_result, false_result) -> None:
        self.divisible_by = divisible_by
        self.true_result = true_result
        self.false_result = false_result

    def throw_to_which_monkey(self, item) -> int:
        if item % self.divisible_by == 0:
            return self.true_result

        return self.false_result


class Monkey:
    def __init__(
        self,
        name: str,
        items: list[int],
        operation: Operation,
        test: Test,
        modulo: Optional[int] = None,
    ) -> None:
        self.name = name
        self.items = items
        self.operation = operation
        self.test = test
        self.modulo = modulo
        self.borred_factor = 3
        self.other_monkeys = {}
        self.inspections = 0

    def add_other_monkey(self, other_monkey):
        self.other_monkeys[other_monkey.name] = other_monkey

    def take_turn(self, part: str):
        def relieve_part_one(item: int):
            # get bored (your relief) factor (part one)
            return item // self.borred_factor

        def relieve_part_two(item: int):
            # take super module, Chinese remainder theorem (part two)
            return item % self.modulo

        relieve_fuctions = {"one": relieve_part_one, "two": relieve_part_two}

        while len(self.items) > 0:
            item = self.items.pop(0)
            # inspect
            item = self.operation.inspect(item)
            self.inspections += 1
            # relieve
            item = relieve_fuctions[part](item=item)
            # test
            other_monkey_name = self.test.throw_to_which_monkey(item)
            # throw to other monkey
            self.other_monkeys[other_monkey_name].catch_item(item)

    def catch_item(self, item):
        self.items.append(item)


def parse_monkeys(lines) -> list[Monkey]:

    monkeys = []
    modulo = 1

    for i in range(0, len(lines), 7):

        monkey_number = lines[i].split("Monkey ")[-1][:-1]
        starting_items = list(
            map(int, lines[i + 1].split("Starting items: ")[-1].split(","))
        )
        operator, arg = lines[i + 2].split("Operation: new = old ")[-1].split()
        divisible_by = int(lines[i + 3].split("Test: divisible by ")[-1])
        true_result = lines[i + 4].split("If true: throw to monkey ")[-1]
        false_result = lines[i + 5].split("If false: throw to monkey ")[-1]

        operation = Operation(operator=operator, arg=arg)
        test = Test(
            divisible_by=divisible_by,
            true_result=true_result,
            false_result=false_result,
        )

        modulo *= divisible_by

        monkey = Monkey(
            name=monkey_number, items=starting_items, operation=operation, test=test
        )

        monkeys.append(monkey)

    # Make sure all monkeys can throw to each other
    for monkey in monkeys:
        for other_monkey in monkeys:
            if other_monkey is monkey:
                continue
            monkey.add_other_monkey(other_monkey)

    # set module
    for monkey in monkeys:
        monkey.modulo = modulo

    return monkeys


def print_worry_levels(printer, round_number, monkeys):
    printer(
        f"After round {round_number}, the monkeys are holding items with these worry levels:"
    )
    for monkey in monkeys:
        printer(f"Monkey {monkey.name}: {monkey.items}")

    printer("")


def print_inspections(printer, monkeys):
    for monkey in monkeys:
        printer(f"Monkey {monkey.name} inspected items {monkey.inspections} times.")


def play_rounds(monkeys: list[Monkey], num_rounds, part):
    for round_number in range(1, num_rounds + 1):
        for monkey in monkeys:
            monkey.take_turn(part=part)

        if part == "one":
            print_worry_levels(logger.debug, round_number, monkeys)

        if part == "two":
            if round_number == 1 or round_number == 20 or round_number % 1000 == 0:
                logger.debug(f"== After round {round_number} ==")
                print_inspections(logger.debug, monkeys)

    if part == "one":
        print_inspections(logger.debug, monkeys)

    monkeys_inspections = sorted([monkey.inspections for monkey in monkeys])
    monkey_business = monkeys_inspections[-1] * monkeys_inspections[-2]

    return monkey_business


def solve_part_one(lines):
    monkeys = parse_monkeys(lines)

    monkey_business = play_rounds(monkeys=monkeys, num_rounds=20, part="one")

    return monkey_business


def solve_part_two(lines):
    monkeys = parse_monkeys(lines)

    monkey_business = play_rounds(monkeys=monkeys, num_rounds=10_000, part="two")

    return monkey_business


def main():

    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    FORMAT = "%(message)s"
    logging.basicConfig(format=FORMAT)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.info("---- Day 11: Monkey in the Middle ---")

    if args.part in ["1", "one", None]:
        answer_part_one = solve_part_one(lines)
        logger.info(f"Answer part one: {answer_part_one}")

    if args.part in ["2", "two", None]:
        logger.info("--- Part Two ---")
        answer_part_two = solve_part_two(lines)
        logger.info(f"Answer part two: {answer_part_two}")


if __name__ == "__main__":
    main()
