from collections import deque


def mix(nums):
    len_nums = len(nums)

    # for each number
    for i in range(len_nums):
        # rotate next number to the front
        while True:
            if nums[0][0] == i:
                break
            nums.append(nums.popleft())

        # get the current one and then rotate to where it goes
        cur = nums.popleft()
        rotate_by = cur[1] % (len_nums - 1)
        for _ in range(rotate_by):
            nums.append(nums.popleft())
        nums.append(cur)

    return nums


def score_nums(nums):
    len_nums = len(nums)
    # get 0 value into first position
    while nums[0][1] != 0:
        nums.append(nums.popleft())

    return sum(nums[c % len_nums][1] for c in [1000, 2000, 3000])


def parse(lines):
    numbers = list(map(int, lines))
    return numbers


def solve_part_one(lines: list[str], example: bool) -> int:

    numbers = parse(lines)

    nums = deque(enumerate(numbers))
    nums = mix(nums)
    return score_nums(nums)


def solve_part_two(lines: list[str], example: bool) -> int:
    numbers = parse(lines)

    nums = deque((i, n * 811589153) for i, n in enumerate(numbers))
    for i in range(10):
        print(f"\r{i}", end="")
        nums = mix(nums)
    return score_nums(nums)
