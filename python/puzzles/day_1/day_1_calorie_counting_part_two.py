

input_file = "day_1_input.txt"
# input_file = "day_1_input_example.txt"

with open(input_file, "r") as fh:
    elf_index = 0
    elf_calories = [0]
    for line in fh.read().splitlines():
        if line == "":
            elf_calories.append(0)
            elf_index += 1
            continue
        calories = int(line)
        elf_calories[elf_index] += calories

    num_elves = len(elf_calories)
    highest_calories = max(elf_calories)

    print(f"Number of elves: {num_elves}")
    print(f"Highest number of calories: {highest_calories}")

    highest_top_three = sorted(elf_calories, reverse=True)[0:3]
    total_top_three = sum(highest_top_three)

    print(f"Total calories top three: {total_top_three}")

