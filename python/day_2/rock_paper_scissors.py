import sys

opponent_shapes = {"A": "Rock", "B": "Paper", "C": "Scissors"}
my_shapes = {"X": "Rock", "Y": "Paper", "Z": "Scissors"}

shape_scores = {"Rock": 1, "Paper": 2, "Scissors": 3}


def calculate_score(opponent_shape, my_shape):
    draw_score = 3
    win_score = 6
    loose_score = 0

    shape_score = shape_scores[my_shape]

    if opponent_shape == my_shape:
        return shape_score + draw_score

    if my_shape == "Rock" and opponent_shape == "Paper":
        return loose_score + shape_score

    if my_shape == "Rock" and opponent_shape == "Scissors":
        return win_score + shape_score

    if my_shape == "Paper" and opponent_shape == "Rock":
        return win_score + shape_score

    if my_shape == "Paper" and opponent_shape == "Scissors":
        return loose_score + shape_score

    if my_shape == "Scissors" and opponent_shape == "Rock":
        return loose_score + shape_score

    if my_shape == "Scissors" and opponent_shape == "Paper":
        return win_score + shape_score


def main(input_file):

    with open(input_file, "r") as fh:
        total_score = 0
        for line in fh.read().splitlines():
            opponent_encrypted_shape, my_encrypted_shape = line.split(" ")

            opponent_shape = opponent_shapes[opponent_encrypted_shape]
            my_shape = my_shapes[my_encrypted_shape]

            score = calculate_score(opponent_shape, my_shape)
            print(line, score)
            total_score += score

        print(f"Total score: {total_score}")


if __name__ == "__main__":
    input_file = "puzzle_input.txt"

    if len(sys.argv) >= 2 and sys.argv[1] == "example":
        print("Using example data")
        input_file = "puzzle_input_example.txt"

    main(input_file)
