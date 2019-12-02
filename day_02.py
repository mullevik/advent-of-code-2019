import fileinput
from typing import List


def compute_add(sequence: List[int],
                first_input: int, second_input: int, output: int) -> None:
    sequence[output] = sequence[first_input] + sequence[second_input]


def compute_multiply(sequence: List[int],
                     first_input: int, second_input: int, output: int) -> None:
    sequence[output] = sequence[first_input] * sequence[second_input]


def process_instructions(instruction_sequence: List[int]):
    for index in range(0, len(instruction_sequence), 4):

        operand = instruction_sequence[index]

        if operand == 99:
            break
        elif operand == 1:
            first_input = instruction_sequence[index + 1]
            second_input = instruction_sequence[index + 2]
            output = instruction_sequence[index + 3]
            compute_add(instruction_sequence, first_input, second_input,
                        output)
        elif operand == 2:
            first_input = instruction_sequence[index + 1]
            second_input = instruction_sequence[index + 2]
            output = instruction_sequence[index + 3]
            compute_multiply(instruction_sequence, first_input, second_input,
                             output)
        else:
            raise ValueError("Unknown operand")


if __name__ == "__main__":
    input_string = input()

    solution = None

    for noun in range(100):
        for verb in range(100):
            program_sequence = [int(x) for x in input_string.split(",")]
            program_sequence[1] = noun
            program_sequence[2] = verb
            process_instructions(program_sequence)

            if program_sequence[0] == 19690720:
                solution = (noun, verb)
                break

    if solution is None:
        raise ValueError("No solution found")

    result = 100 * solution[0] + solution[1]
    print("Result is:", result)
