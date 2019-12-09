import fileinput
from enum import IntEnum
from typing import List, NamedTuple, Dict
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
        return input()

    # def output(self, x: str):
    #     self.io_queue.append(x)
    #     print(x)

    def output(self, x: str):
        print(x)


class Argument(object):
    address: int

    def __init__(self, address: int):
        self.address = address

    def value(self, sequence: Dict[int, int], relative_base=None) -> int:
        raise NotImplementedError

    def get_address(self, relative_base=None):
        raise NotImplementedError


class ImmediateArgument(Argument):

    def value(self, sequence: Dict[int, int], relative_base=None) -> int:
        return self.address

    def get_address(self, relative_base=None):
        raise ValueError("Immeadiate argument should not do this")


class AddressedArgument(Argument):

    def value(self, sequence: Dict[int, int], relative_base=None) -> int:
        if self.address not in sequence:
            return 0
        return sequence[self.address]

    def get_address(self, relative_base=None):
        return self.address


class RelativeAddressedArgument(Argument):

    def value(self, sequence: Dict[int, int], relative_base: int = None) -> int:
        if relative_base is None:
            raise ValueError("relative base should not be none!")
        if self.address + relative_base not in sequence:
            return 0
        return sequence[self.address + relative_base]

    def get_address(self, relative_base=None):
        if relative_base is None:
            raise ValueError("relative base should not be none!")
        return self.address + relative_base


def compute_add(sequence: Dict[int, int],
                in1: Argument, in2: Argument, out: Argument, rb: int) -> None:
    sequence[out.get_address(rb)] = in1.value(sequence, rb) \
                            + in2.value(sequence, rb)


def compute_multiply(sequence: Dict[int, int],
                     in1: Argument, in2: Argument, out: Argument, rb: int) -> None:
    sequence[out.get_address(rb)] = in1.value(sequence, rb) \
                                        * in2.value(sequence, rb)


def take_input(sequence: Dict[int, int], out: Argument, io: CustomIO, rb: int):
    input_value = int(io.input())
    sequence[out.get_address(rb)] = input_value


def print_output(sequence: Dict[int, int], in1: Argument, io: CustomIO, rb: int):
    io.output(str(in1.value(sequence, rb)))


def jump_if_true(sequence: Dict[int, int], in1: Argument, in2: Argument,
                 program_counter: int, rb: int) -> int:
    if in1.value(sequence, rb) != 0:
        return in2.value(sequence, rb)
    else:
        return program_counter + 3


def jump_if_false(sequence: Dict[int, int], in1: Argument, in2: Argument,
                  program_counter: int, rb: int) -> int:
    if in1.value(sequence, rb) == 0:
        return in2.value(sequence, rb)
    else:
        return program_counter + 3


def less_than(sequence: Dict[int, int], in1: Argument, in2: Argument,
              out: Argument, rb: int):
    if in1.value(sequence, rb) < in2.value(sequence, rb):
        sequence[out.get_address(rb)] = 1
    else:
        sequence[out.get_address(rb)] = 0


def equals(sequence: Dict[int, int], in1: Argument, in2: Argument, out: Argument,
           rb: int):
    if in1.value(sequence, rb) == in2.value(sequence, rb):
        sequence[out.get_address(rb)] = 1
    else:
        sequence[out.get_address(rb)] = 0


def adjust_relative_base(sequence: Dict[int, int], in1: Argument,
                         rb: int):
    return rb + in1.value(sequence, rb)


def create_argument(state, address):
    if state == "0":
        return AddressedArgument(address=address)
    elif state == "1":
        return ImmediateArgument(address=address)
    elif state == "2":
        return RelativeAddressedArgument(address=address)
    else:
        raise ValueError("Unknown argument type")


def process_instructions(instruction_sequence: List[int], io: CustomIO):
    # for index in range(0, len(instruction_sequence), 4):

    program_counter = 0
    relative_base = 0

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
            compute_add(instruction_sequence, in1, in2, out, relative_base)
            program_counter += 4

        elif operand == 2:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            out = create_argument(states[2],
                                  instruction_sequence[program_counter + 3])
            compute_multiply(instruction_sequence, in1, in2, out, relative_base)
            program_counter += 4
        elif operand == 3:
            out = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            take_input(instruction_sequence, out, io, relative_base)
            program_counter += 2
        elif operand == 4:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            print_output(instruction_sequence, in1, io, relative_base)
            program_counter += 2
        elif operand == 5:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            program_counter = jump_if_true(instruction_sequence, in1, in2,
                                           program_counter, relative_base)
        elif operand == 6:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            program_counter = jump_if_false(instruction_sequence, in1, in2,
                                            program_counter, relative_base)
        elif operand == 7:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            out = create_argument(states[2],
                                  instruction_sequence[program_counter + 3])
            less_than(instruction_sequence, in1, in2, out, relative_base)
            program_counter += 4
        elif operand == 8:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            in2 = create_argument(states[1],
                                  instruction_sequence[program_counter + 2])
            out = create_argument(states[2],
                                  instruction_sequence[program_counter + 3])
            equals(instruction_sequence, in1, in2, out, relative_base)
            program_counter += 4
        elif operand == 9:
            in1 = create_argument(states[0],
                                  instruction_sequence[program_counter + 1])
            relative_base = adjust_relative_base(instruction_sequence, in1,
                                                 relative_base)
            program_counter += 2
        else:
            raise ValueError("Unknown operand" + operand)


if __name__ == "__main__":
    input_string = input()

    program_sequence = [int(x) for x in input_string.split(",")]

    program_dict = {}
    for address, value in enumerate(program_sequence):
        program_dict[address] = value

    io = CustomIO()
    process_instructions(program_dict, io)

"""
1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,1,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,1,21,1004,1101,28,0,1016,1101,0,27,1010,1102,36,1,1008,1102,33,1,1013,1101,0,22,1012,1101,0,37,1011,1102,34,1,1017,1102,466,1,1027,1102,1,484,1029,1102,1,699,1024,1102,1,1,1021,1101,0,0,1020,1102,1,24,1015,1101,0,473,1026,1101,653,0,1022,1102,26,1,1007,1102,25,1,1006,1101,0,39,1014,1102,646,1,1023,1101,690,0,1025,1102,1,29,1019,1101,32,0,1018,1101,30,0,1002,1101,0,20,1001,1102,1,38,1005,1102,1,23,1003,1101,0,31,1000,1101,35,0,1009,1101,0,493,1028,109,5,1208,0,37,63,1005,63,201,1001,64,1,64,1106,0,203,4,187,1002,64,2,64,109,-4,2107,36,8,63,1005,63,223,1001,64,1,64,1105,1,225,4,209,1002,64,2,64,109,18,21107,40,41,-9,1005,1010,243,4,231,1105,1,247,1001,64,1,64,1002,64,2,64,109,6,21107,41,40,-9,1005,1016,267,1001,64,1,64,1106,0,269,4,253,1002,64,2,64,109,-19,21102,42,1,5,1008,1011,42,63,1005,63,291,4,275,1105,1,295,1001,64,1,64,1002,64,2,64,109,15,1205,0,309,4,301,1105,1,313,1001,64,1,64,1002,64,2,64,109,-27,2101,0,9,63,1008,63,20,63,1005,63,333,1106,0,339,4,319,1001,64,1,64,1002,64,2,64,109,19,21102,43,1,6,1008,1019,45,63,1005,63,363,1001,64,1,64,1105,1,365,4,345,1002,64,2,64,109,1,21108,44,47,-3,1005,1011,385,1001,64,1,64,1106,0,387,4,371,1002,64,2,64,109,-22,1201,9,0,63,1008,63,21,63,1005,63,411,1001,64,1,64,1106,0,413,4,393,1002,64,2,64,109,9,1207,0,19,63,1005,63,433,1001,64,1,64,1106,0,435,4,419,1002,64,2,64,109,-9,2107,30,8,63,1005,63,453,4,441,1105,1,457,1001,64,1,64,1002,64,2,64,109,25,2106,0,10,1001,64,1,64,1106,0,475,4,463,1002,64,2,64,109,11,2106,0,0,4,481,1001,64,1,64,1105,1,493,1002,64,2,64,109,-18,2108,21,-6,63,1005,63,511,4,499,1106,0,515,1001,64,1,64,1002,64,2,64,109,-12,2108,18,6,63,1005,63,535,1001,64,1,64,1106,0,537,4,521,1002,64,2,64,109,19,21101,45,0,-7,1008,1010,45,63,1005,63,563,4,543,1001,64,1,64,1105,1,563,1002,64,2,64,109,-10,1207,-5,31,63,1005,63,581,4,569,1106,0,585,1001,64,1,64,1002,64,2,64,109,-8,2102,1,5,63,1008,63,21,63,1005,63,611,4,591,1001,64,1,64,1105,1,611,1002,64,2,64,109,5,1201,0,0,63,1008,63,21,63,1005,63,633,4,617,1106,0,637,1001,64,1,64,1002,64,2,64,109,13,2105,1,6,1001,64,1,64,1106,0,655,4,643,1002,64,2,64,109,-7,1202,-3,1,63,1008,63,26,63,1005,63,681,4,661,1001,64,1,64,1106,0,681,1002,64,2,64,109,12,2105,1,2,4,687,1001,64,1,64,1105,1,699,1002,64,2,64,109,-28,1208,8,30,63,1005,63,717,4,705,1106,0,721,1001,64,1,64,1002,64,2,64,109,10,1202,1,1,63,1008,63,40,63,1005,63,745,1001,64,1,64,1105,1,747,4,727,1002,64,2,64,109,10,21108,46,46,-2,1005,1012,765,4,753,1105,1,769,1001,64,1,64,1002,64,2,64,109,-2,1205,8,781,1106,0,787,4,775,1001,64,1,64,1002,64,2,64,109,-9,2101,0,0,63,1008,63,23,63,1005,63,809,4,793,1105,1,813,1001,64,1,64,1002,64,2,64,109,9,1206,8,831,4,819,1001,64,1,64,1106,0,831,1002,64,2,64,109,-9,2102,1,-2,63,1008,63,22,63,1005,63,855,1001,64,1,64,1106,0,857,4,837,1002,64,2,64,109,4,21101,47,0,10,1008,1017,50,63,1005,63,877,1105,1,883,4,863,1001,64,1,64,1002,64,2,64,109,18,1206,-4,895,1105,1,901,4,889,1001,64,1,64,4,64,99,21101,0,27,1,21102,915,1,0,1106,0,922,21201,1,56639,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,1,942,0,1106,0,922,22102,1,1,-1,21201,-2,-3,1,21101,0,957,0,1106,0,922,22201,1,-1,-2,1106,0,968,22102,1,-2,-2,109,-3,2106,0,0
"""