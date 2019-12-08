import fileinput
from enum import IntEnum
from typing import List, NamedTuple
import itertools


class CustomIO(object):
    io_queue: List[str]
    stdin: List[str]
    stdout: List[str]

    def __init__(self):
        self.io_queue = []
        self.stdin = []
        self.stdout = []

    # def input(self) -> str:
    #     if not self.io_queue:
    #         return input()
    #     return self.io_queue.pop(0)

    def input(self) -> str:
        return self.stdin.pop(0)

    # def output(self, x: str):
    #     self.io_queue.append(x)
    #     print(x)

    def output(self, x: str):
        self.stdout.append(x)
        print(x)


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


def take_input(sequence: List[int], out: Argument, io: CustomIO):
    input_value = int(io.input())
    sequence[out.address] = input_value


def print_output(sequence: List[int], in1: Argument, io: CustomIO):
    io.output(str(in1.value(sequence)))


def jump_if_true(sequence: List[int], in1: Argument, in2: Argument,
                 program_counter: int) -> int:
    if in1.value(sequence) != 0:
        return in2.value(sequence)
    else:
        return program_counter + 3


def jump_if_false(sequence: List[int], in1: Argument, in2: Argument,
                  program_counter: int) -> int:
    if in1.value(sequence) == 0:
        return in2.value(sequence)
    else:
        return program_counter + 3


def less_than(sequence: List[int], in1: Argument, in2: Argument,
              out: Argument):
    if in1.value(sequence) < in2.value(sequence):
        sequence[out.address] = 1
    else:
        sequence[out.address] = 0


def equals(sequence: List[int], in1: Argument, in2: Argument, out: Argument):
    if in1.value(sequence) == in2.value(sequence):
        sequence[out.address] = 1
    else:
        sequence[out.address] = 0


def create_argument(state, address):
    if state == "0":
        return AddressedArgument(address=address)
    else:
        return ImmediateArgument(address=address)


def process_instructions(instruction_sequence: List[int], io: CustomIO):
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
            take_input(instruction_sequence, out, io)
            program_counter += 2
        elif operand == 4:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            print_output(instruction_sequence, in1, io)
            program_counter += 2
        elif operand == 5:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            program_counter = jump_if_true(instruction_sequence, in1, in2,
                                           program_counter)
        elif operand == 6:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            program_counter = jump_if_false(instruction_sequence, in1, in2,
                                            program_counter)
        elif operand == 7:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            out = create_argument(states[2],
                                  instruction_sequence[program_counter + 3])
            less_than(instruction_sequence, in1, in2, out)
            program_counter += 4
        elif operand == 8:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            out = create_argument(states[2],
                                  instruction_sequence[program_counter + 3])
            equals(instruction_sequence, in1, in2, out)
            program_counter += 4
        else:
            raise ValueError("Unknown operand" + operand)


if __name__ == "__main__":
    input_string = input()

    phases = [9,8,7,6,5]

    all_phases = itertools.permutations(phases)

    biggest_amplifier_output = 0

    # for phase_sequence in all_phases:
    program_sequence = [int(x) for x in input_string.split(",")]

    amplifier_output = ["0"]

    print(amplifier_output)

    for phase in phases:
        io = CustomIO()
        io.stdin = [phase] + amplifier_output
        process_instructions(program_sequence, io)
        amplifier_output = io.stdout

    print(amplifier_output)

    #     if amplifier_output > biggest_amplifier_output:
    #         biggest_amplifier_output = amplifier_output
    #
    # print(biggest_amplifier_output)

"""
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0

3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0

3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5

3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
"""