from aoc_2022.utils import utils


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
    def __init__(self, name, items, operation, test) -> None:
        self.name = name
        self.items = items
        self.operation = operation
        self.test = test
        self.other_monkeys = {}
        self.inspections = 0

    def add_other_monkey(self, other_monkey):
        self.other_monkeys[other_monkey.name] = other_monkey

    def take_turn(self):
        # breakpoint()
        while self.items:
            item = self.items.pop(0)
            # inspect
            item = self.operation.inspect(item)
            self.inspections += 1
            # get bored
            item //= 3
            # test
            other_monkey_name = self.test.throw_to_which_monkey(item)
            # throw to other monkey
            self.other_monkeys[other_monkey_name].catch_item(item)

    def catch_item(self, item):
        self.items.append(item)


def parse_monkeys(lines) -> list[Monkey]:

    monkeys = []

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
        monkey = Monkey(
            name=monkey_number, items=starting_items, operation=operation, test=test
        )

        monkeys.append(monkey)

    #
    for monkey in monkeys:
        for other_monkey in monkeys:
            if other_monkey is monkey:
                continue
            monkey.add_other_monkey(other_monkey)

    return monkeys


def solve_part_one(lines):
    monkeys = parse_monkeys(lines)

    for round in range(20):
        for monkey in monkeys:
            monkey.take_turn()

        print(
            f"After round {round}, the monkeys are holding items with these worry levels:"
        )
        for monkey in monkeys:
            print(f"Monkey {monkey.name}: {monkey.items}")

    print()
    for monkey in monkeys:
        print(f"Monkey {monkey.name} inspected items {monkey.inspections} times.")

    monkeys_inspections = sorted([monkey.inspections for monkey in monkeys])
    monkey_business = monkeys_inspections[-1] * monkeys_inspections[-2]

    return monkey_business


def solve_part_two(lines):
    pass


def main():

    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("---- Day 11: Monkey in the Middle ---")
    answer_part_one = solve_part_one(lines)
    print(f"Answer part one: {answer_part_one}")

    print("--- Part Two ---")
    answer_part_two = solve_part_two(lines)
    print(f"Answer part two: {answer_part_two}")


if __name__ == "__main__":
    main()
