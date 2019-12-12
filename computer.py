import fileinput
from enum import IntEnum
from typing import List, NamedTuple, Dict
import itertools


class IO(object):

    def input(self) -> str:
        raise NotImplementedError

    def output(self, out: str) -> None:
        raise NotImplementedError


class Argument(object):
    address_index: int

    def __init__(self, address: int):
        self.address_index = address

    def value(self, computer: 'IntCodeComputer') -> int:
        raise NotImplementedError

    def address(self, computer: 'IntCodeComputer'):
        raise NotImplementedError


class ImmediateArgument(Argument):

    def value(self, computer: 'IntCodeComputer') -> int:
        return self.address_index

    def address(self, computer: 'IntCodeComputer'):
        raise ValueError("Immeadiate argument should not do this")


class AddressedArgument(Argument):

    def value(self, computer: 'IntCodeComputer') -> int:
        return computer.memory[self.address_index]

    def address(self, computer: 'IntCodeComputer'):
        return self.address_index


class RelativeAddressedArgument(Argument):

    def value(self, computer: 'IntCodeComputer') -> int:
        return computer.memory[self.address_index + computer.rb]

    def address(self, computer: 'IntCodeComputer'):
        return self.address_index + computer.rb


class RandomAccessMemory(object):
    """A RAM for the IntComputer"""
    memory: Dict[int, int]
    uninitialized_memory_value: int

    def __init__(self, program_sequence: List[int]):
        self.uninitialized_memory_value = 0

        self.memory = {}
        for address, value in enumerate(program_sequence):
            self.memory[address] = value

    def __getitem__(self, key):
        if key not in self.memory:
            return self.uninitialized_memory_value
        return self.memory[key]

    def __setitem__(self, key, value):
        self.memory[key] = value


class IntCodeComputer(object):
    pc: int  # the program counter register
    rb: int  # the relative base register
    halt: bool  # halting register
    memory: RandomAccessMemory  # random access memory
    io: IO

    def __init__(self, program_sequence: List[int], io: IO):
        self.pc = 0
        self.rb = 0
        self.halt = False

        self.memory = RandomAccessMemory(program_sequence)
        self.io = io

    @staticmethod
    def create_argument(state: str, address: int):
        if state == "0":
            return AddressedArgument(address=address)
        elif state == "1":
            return ImmediateArgument(address=address)
        elif state == "2":
            return RelativeAddressedArgument(address=address)
        else:
            raise ValueError("Unknown argument type")

    def run(self):
        while not self.halt:
            instruction = self.memory[self.pc]
            self.process_instruction(instruction)

    def process_instruction(self, instruction: int):
        instruction = str(instruction)

        operand = int(instruction[-2:])

        # take leading chars up to operand and reverse it and append zeroes
        states = instruction[:-2]
        states = states[::-1] + "000000000000000"

        if operand == 99:
            self.halt = True
        if operand == 1:
            in1 = self.create_argument(states[0],
                                       self.memory[self.pc + 1])
            in2 = self.create_argument(states[1],
                                       self.memory[self.pc + 2])
            out = self.create_argument(states[2],
                                       self.memory[self.pc + 3])
            self.instruction_add(in1, in2, out)
        if operand == 2:
            in1 = self.create_argument(states[0],
                                       self.memory[self.pc + 1])
            in2 = self.create_argument(states[1],
                                       self.memory[self.pc + 2])
            out = self.create_argument(states[2],
                                       self.memory[self.pc + 3])
            self.instruction_multiply(in1, in2, out)
        if operand == 3:
            out = self.create_argument(states[0], self.memory[self.pc + 1])
            self.instruction_input(out)
        if operand == 4:
            in1 = self.create_argument(states[0], self.memory[self.pc + 1])
            self.instruction_output(in1)
        if operand == 5:
            in1 = self.create_argument(states[0], self.memory[self.pc + 1])
            in2 = self.create_argument(states[1], self.memory[self.pc + 2])
            self.instruction_jump_if_true(in1, in2)
        if operand == 6:
            in1 = self.create_argument(states[0], self.memory[self.pc + 1])
            in2 = self.create_argument(states[1], self.memory[self.pc + 2])
            self.instruction_jump_if_false(in1, in2)
        if operand == 7:
            in1 = self.create_argument(states[0],
                                       self.memory[self.pc + 1])
            in2 = self.create_argument(states[1],
                                       self.memory[self.pc + 2])
            out = self.create_argument(states[2],
                                       self.memory[self.pc + 3])
            self.instruction_less_than(in1, in2, out)
        if operand == 8:
            in1 = self.create_argument(states[0],
                                       self.memory[self.pc + 1])
            in2 = self.create_argument(states[1],
                                       self.memory[self.pc + 2])
            out = self.create_argument(states[2],
                                       self.memory[self.pc + 3])
            self.instruction_equals(in1, in2, out)
        if operand == 9:
            in1 = self.create_argument(states[0],
                                       self.memory[self.pc + 1])
            self.instruction_adjust_rb(in1)

    def instruction_add(self, in1: Argument, in2: Argument, out: Argument):
        self.memory[out.address(self)] = in1.value(self) + in2.value(self)
        self.pc += 4

    def instruction_multiply(self, in1: Argument, in2: Argument,
                             out: Argument):
        self.memory[out.address(self)] = in1.value(self) * in2.value(self)
        self.pc += 4

    def instruction_input(self, out: Argument):
        input_value = int(self.io.input())
        self.memory[out.address(self)] = input_value
        self.pc += 2

    def instruction_output(self, in1: Argument):
        self.io.output(str(in1.value(self)))
        self.pc += 2

    def instruction_jump_if_true(self, in1: Argument, in2: Argument):
        if in1.value(self) != 0:
            self.pc = in2.value(self)
        else:
            self.pc += 3

    def instruction_jump_if_false(self, in1: Argument, in2: Argument):
        if in1.value(self) == 0:
            self.pc = in2.value(self)
        else:
            self.pc += 3

    def instruction_less_than(self, in1: Argument, in2: Argument,
                              out: Argument):
        if in1.value(self) < in2.value(self):
            self.memory[out.address(self)] = 1
        else:
            self.memory[out.address(self)] = 0
        self.pc += 4

    def instruction_equals(self, in1: Argument, in2: Argument, out: Argument):
        if in1.value(self) == in2.value(self):
            self.memory[out.address(self)] = 1
        else:
            self.memory[out.address(self)] = 0
        self.pc += 4

    def instruction_adjust_rb(self, in1: Argument):
        self.rb += in1.value(self)
        self.pc += 2


def scan_program_from_input() -> List[int]:
    """Scans one input line and creates a program sequence from it."""
    input_string = input()
    return [int(x) for x in input_string.split(",")]


def main():
    program_sequence = scan_program_from_input()
    computer = IntCodeComputer(program_sequence, None)
    computer.run()


if __name__ == "__main__":
    main()
