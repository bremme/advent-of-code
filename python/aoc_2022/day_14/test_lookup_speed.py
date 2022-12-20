from collections import namedtuple
from dataclasses import dataclass
from timeit import timeit


@dataclass(frozen=True)
class DataclassCoordinate:
    row: int
    column: int


class NormalClassCoordinate:
    def __init__(self, row, column) -> None:
        self.row = row
        self.column = column


NamedTupleCoordinate = namedtuple("NamedTupleCoordinate", ["row", "column"])


def test_dataclass_set():
    Constructor = DataclassCoordinate
    data = set()
    data.update([Constructor(row, col) for row, col in zip(range(1000), range(1000))])
    coordinate = Constructor(1, 1)

    return timeit(lambda: coordinate in data)


def test_normalclass_set():
    Constructor = NormalClassCoordinate
    data = set()
    data.update([Constructor(row, col) for row, col in zip(range(1000), range(1000))])
    coordinate = Constructor(1, 1)

    return timeit(lambda: coordinate in data)


def test_namedtuple_set():
    Constructor = NamedTupleCoordinate
    data = set()
    data.update([Constructor(row, col) for row, col in zip(range(1000), range(1000))])
    coordinate = Constructor(1, 1)

    return timeit(lambda: coordinate in data)


def test_tuple_set():
    Constructor = tuple
    data = set()
    data.update([Constructor([row, col]) for row, col in zip(range(1000), range(1000))])
    coordinate = Constructor([1, 1])

    return timeit(lambda: coordinate in data)


def test_tuple_dict():
    Constructor = tuple
    data = {(row, col): "#" for row, col in zip(range(1000), range(1000))}
    coordinate = Constructor([1, 1])

    return timeit(lambda: coordinate in data)


def main():
    print(f"{test_dataclass_set()} (test_dataclass_set)")
    print(f"{test_normalclass_set()} (test_normalclass_set)")
    print(f"{test_namedtuple_set()} (test_namedtuple_set)")
    print(f"{test_tuple_set()} (test_tuple_set)")
    print(f"{test_tuple_dict()} (test_tuple_dict)")


if __name__ == "__main__":

    main()
