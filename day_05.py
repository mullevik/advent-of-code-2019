import fileinput
from enum import IntEnum
from typing import List, NamedTuple


class Argument(object):
    address: int

    def __init__(self, address: int):
        self.address = address

    def value(self, sequence: List[int]):
        raise NotImplementedError


class ImmediateArgument(Argument):

    def value(self, sequence: List[int]):
        return self.address


class AddressedArgument(Argument):

    def value(self, sequence: List[int]):
        return sequence[self.address]


def compute_add(sequence: List[int],
                in1: Argument, in2: Argument, out: Argument) -> None:
    sequence[out.address] = in1.value(sequence) + in2.value(sequence)


def compute_multiply(sequence: List[int],
                     in1: Argument, in2: Argument, out: Argument) -> None:
    sequence[out.address] = in1.value(sequence) * in2.value(sequence)


def take_input(sequence: List[int], out: Argument):
    input_value = int(input())
    sequence[out.address] = input_value


def print_output(sequence: List[int], in1: Argument):
    print(in1.value(sequence))


def create_argument(state, address):
    if state == "0":
        return AddressedArgument(address=address)
    else:
        return ImmediateArgument(address=address)


def process_instructions(instruction_sequence: List[int]):
    # for index in range(0, len(instruction_sequence), 4):

    program_counter = 0

    while True:
        instruction = str(instruction_sequence[program_counter])

        operand = int(instruction[-2:])

        # take leading chars up to operand and reverse it and append zeroes
        states = instruction[:-2]
        states = states[::-1] + "000000000000000"

        if operand == 99:
            break
        elif operand == 1:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            out = create_argument(states[2],
                                  instruction_sequence[program_counter + 3])
            compute_add(instruction_sequence, in1, in2, out)
            program_counter += 4

        elif operand == 2:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            out = create_argument(states[2],
                                  instruction_sequence[program_counter + 3])
            compute_multiply(instruction_sequence, in1, in2, out)
            program_counter += 4
        elif operand == 3:
            out = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            take_input(instruction_sequence, out)
            program_counter += 2
        elif operand == 4:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            print_output(instruction_sequence, in1)
            program_counter += 2
        else:
            raise ValueError("Unknown operand" + operand)


if __name__ == "__main__":
    input_string = input()
    program_sequence = [int(x) for x in input_string.split(",")]
    process_instructions(program_sequence)
