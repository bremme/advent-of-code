import sys
from pathlib import Path


class FileSystemObject:
    def __init__(self, name, is_directory):
        self.name = name
        self.is_directory = is_directory


class File(FileSystemObject):
    def __init__(self, name, size):
        super().__init__(name=name, is_directory=False)
        self.size = size


class Directory(FileSystemObject):
    def __init__(self, name):
        super().__init__(name=name, is_directory=True)
        self.content: dict[str, FileSystemObject] = {".": self, "..": None}

    def add_file_system_object(self, file_system_object: FileSystemObject):
        self.content[file_system_object.name] = file_system_object

    def calculate_size(self):
        size = 0

        for name, file_system_object in self.content.items():

            if name in [".", ".."]:
                continue

            if file_system_object.is_directory is False:
                size += file_system_object.size
            else:
                size += file_system_object.calculate_size()

        return size

    def get_directory(self, name):
        directory = self.content.get(name, None)

        if directory is None or directory.is_directory is False:
            raise KeyError(f"No directory with name '{name}")

        return directory

    def get_child_directories(self):
        child_directories = []
        for name, file_system_object in self.content.items():

            if name in [".", ".."]:
                continue

            if file_system_object.is_directory is False:
                continue

            child_directories.append(file_system_object)

        return child_directories

    def add_parent_directory(self, directory):
        self.content[".."] = directory

    def get_parent_directory(self):
        return self.content[".."]


def find_root(directory: Directory):
    cwd = directory
    while cwd.get_parent_directory() is not None:
        cwd = directory.get_parent_directory()

    return cwd


def parse_commands(lines) -> list[tuple[str, list]]:
    commands_and_output = []
    command_index = None

    for line in lines:
        if line.startswith("$"):
            command = line.replace("$ ", "").strip()
            commands_and_output.append((command, []))
            command_index = 0 if command_index is None else command_index + 1
            continue

        output = line.strip()

        commands_and_output[command_index][1].append(output)

    return commands_and_output


def parse_puzzle_input(lines: list[str]) -> Directory:

    commands_and_output = parse_commands(lines)

    cwd = None

    for command, output in commands_and_output:
        if command.startswith("cd"):
            name = command.split()[1]

            if cwd is None:
                cwd = Directory(name)
            elif name == "..":
                cwd = cwd.get_parent_directory()
            else:
                cwd.get_directory(name).add_parent_directory(cwd)
                cwd = cwd.get_directory(name)

        if command.startswith("ls"):
            # get directory listing
            for entry in output:
                if entry.startswith("dir"):
                    name = entry.split()[-1]
                    file_system_object = Directory(name)
                else:
                    size = int(entry.split()[0])
                    name = "".join(entry.split()[1:])
                    file_system_object = File(name, size)
                cwd.add_file_system_object(file_system_object)

    return find_root(cwd)


def find_directories_with_size(directory: Directory, threshold, comparison):
    result = {}

    size = directory.calculate_size()

    if comparison == "ge" and size >= threshold:
        result[directory] = size

    if comparison == "le" and size <= threshold:
        result[directory] = size

    for child_directory in directory.get_child_directories():
        result |= find_directories_with_size(child_directory, threshold, comparison)

    return result


def part_one(lines):
    root = parse_puzzle_input(lines)
    maximum_size = 100_000

    small_directories = find_directories_with_size(root, maximum_size, "le")

    sum_of_small_directories = sum(list(small_directories.values()))

    print(sum_of_small_directories)


def part_two(lines):
    total_disk_space = 70_000_000
    required_free_space = 30_000_000

    root = parse_puzzle_input(lines)
    total_used_space = root.calculate_size()
    free_space = total_disk_space - total_used_space

    minimum_space_to_delete = required_free_space - free_space

    large_directories = find_directories_with_size(root, minimum_space_to_delete, "ge")

    size__of_directory_to_delete = min([size for size in large_directories.values()])

    print(size__of_directory_to_delete)


def main(input_file):
    input_file_path = Path(__file__).with_name(input_file)

    with open(input_file_path, "r") as fh:
        lines = [line for line in fh.read().splitlines()]

    part_one(lines)
    part_two(lines)


if __name__ == "__main__":
    input_file = "puzzle_input.txt"

    if len(sys.argv) >= 2 and sys.argv[1] == "example":
        print("Using example data")
        input_file = "puzzle_input_example.txt"

    main(input_file)


# 47052440 too high
