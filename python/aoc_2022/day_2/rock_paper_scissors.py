from aoc_2022 import utils

opponent_shapes = {"A": "Rock", "B": "Paper", "C": "Scissors"}

my_shapes = {"X": "Rock", "Y": "Paper", "Z": "Scissors"}

shape_scores = {"Rock": 1, "Paper": 2, "Scissors": 3}

outcomes = {"X": "lose", "Y": "draw", "Z": "win"}


def calculate_score(opponent_shape, my_shape):
    draw_score = 3
    win_score = 6
    lose_score = 0

    shape_score = shape_scores[my_shape]

    if opponent_shape == my_shape:
        return shape_score + draw_score

    if my_shape == "Rock" and opponent_shape == "Paper":
        return lose_score + shape_score

    if my_shape == "Rock" and opponent_shape == "Scissors":
        return win_score + shape_score

    if my_shape == "Paper" and opponent_shape == "Rock":
        return win_score + shape_score

    if my_shape == "Paper" and opponent_shape == "Scissors":
        return lose_score + shape_score

    if my_shape == "Scissors" and opponent_shape == "Rock":
        return lose_score + shape_score

    if my_shape == "Scissors" and opponent_shape == "Paper":
        return win_score + shape_score


def determine_shape(opponent_shape, outcome):
    if outcome == "draw":
        return opponent_shape

    if outcome == "win" and opponent_shape == "Rock":
        return "Paper"

    if outcome == "win" and opponent_shape == "Paper":
        return "Scissors"

    if outcome == "win" and opponent_shape == "Scissors":
        return "Rock"

    if outcome == "lose" and opponent_shape == "Rock":
        return "Scissors"

    if outcome == "lose" and opponent_shape == "Paper":
        return "Rock"

    if outcome == "lose" and opponent_shape == "Scissors":
        return "Paper"


def solve_part_one(lines):
    total_score = 0

    for line in lines:
        opponent_encrypted_shape, my_encrypted_shape = line.split(" ")

        opponent_shape = opponent_shapes[opponent_encrypted_shape]
        my_shape = my_shapes[my_encrypted_shape]

        score = calculate_score(opponent_shape, my_shape)
        # print(line, score)
        total_score += score

    return total_score


def solve_part_two(lines):
    total_score = 0

    for line in lines:
        opponent_encrypted_shape, encrypted_outcome = line.split(" ")

        opponent_shape = opponent_shapes[opponent_encrypted_shape]
        outcome = outcomes[encrypted_outcome]

        my_shape = determine_shape(opponent_shape, outcome)

        score = calculate_score(opponent_shape, my_shape)
        # print(line, score)
        total_score += score

    return total_score


def main(input_file):

    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 2: Rock Paper Scissors ---")
    total_score_part_one = solve_part_one(lines)
    print(f"Total score: {total_score_part_one}")

    print("--- Part Two ---")
    total_score_part_two = solve_part_two(lines)
    print(f"Total score: {total_score_part_two}")


if __name__ == "__main__":
    main()
