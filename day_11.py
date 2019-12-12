from collections import defaultdict
from enum import IntEnum
from typing import Dict, List, Set

from computer import IntCodeComputer, IO, scan_program_from_input
from mapping import C2


class Rotation(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def modus():
        return 4


class Color(IntEnum):
    BLACK = 0
    WHITE = 1


class Map(object):
    map: Dict[C2, Color]
    robot_coordinates: C2
    robot_rotation: Rotation
    painted_panels: Set[C2]

    def __init__(self):
        self.map = defaultdict(lambda: Color.BLACK)
        self.robot_coordinates = C2(0, 0)
        self.robot_rotation = Rotation.UP
        self.painted_panels = set()

    def current_color(self) -> Color:
        return self.map[self.robot_coordinates]

    def paint(self, color: Color):
        self.map[self.robot_coordinates] = color
        self.painted_panels.add(self.robot_coordinates)

    def set_paint(self, color: Color):
        self.map[self.robot_coordinates] = color

    def rotate_right_by_90(self):
        self.robot_rotation = Rotation(
            (self.robot_rotation + 1) % Rotation.modus())

    def rotate_left_by_90(self):
        self.robot_rotation = Rotation(
            (self.robot_rotation - 1) % Rotation.modus())

    def step_forward(self):
        if self.robot_rotation == Rotation.UP:
            self.robot_coordinates = C2(self.robot_coordinates.x,
                                        self.robot_coordinates.y - 1)
        elif self.robot_rotation == Rotation.RIGHT:
            self.robot_coordinates = C2(self.robot_coordinates.x + 1,
                                        self.robot_coordinates.y)
        elif self.robot_rotation == Rotation.DOWN:
            self.robot_coordinates = C2(self.robot_coordinates.x,
                                        self.robot_coordinates.y + 1)
        elif self.robot_rotation == Rotation.LEFT:
            self.robot_coordinates = C2(self.robot_coordinates.x - 1,
                                        self.robot_coordinates.y)

    def print(self):
        max_x = self.robot_coordinates.x
        min_x = max_x
        max_y = self.robot_coordinates.y
        min_y = max_y
        for coordinates in self.map.keys():
            if coordinates.x > max_x:
                max_x = coordinates.x
            if coordinates.x < min_x:
                min_x = coordinates.x
            if coordinates.y > max_y:
                max_y = coordinates.y
            if coordinates.y < min_y:
                min_y = coordinates.y

        for y in range(min_y, max_y + 1):
            row = ""
            for x in range(min_x, max_x + 1):
                color = self.map[C2(x, y)]
                if color == Color.BLACK:
                    row += "."
                else:
                    row += "#"
            print(row)


class MapIO(IO):
    map: Map
    outputs: List[str]

    def __init__(self, the_map: Map):
        self.map = the_map
        self.outputs = []

    def input(self) -> str:
        return str(self.map.current_color().value)

    def output(self, out: str) -> None:
        self.outputs.append(out)

        if len(self.outputs) == 2:
            color = Color(int(self.outputs.pop(0)))
            rotation = self.outputs.pop(0)
            self.map.paint(color)
            if rotation == "0":
                self.map.rotate_left_by_90()
            elif rotation == "1":
                self.map.rotate_right_by_90()
            else:
                raise ValueError("Unknown rotation", rotation)
            self.map.step_forward()


def main():

    the_map = Map()
    the_map.set_paint(Color.WHITE)
    cpu = IntCodeComputer(scan_program_from_input(), MapIO(the_map))

    cpu.run()

    print(len(the_map.painted_panels))

    the_map.print()

if __name__ == '__main__':
    main()


"""
3,8,1005,8,319,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1001,8,0,28,2,1008,7,10,2,4,17,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,59,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,81,1006,0,24,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,105,2,6,13,10,1006,0,5,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,134,2,1007,0,10,2,1102,20,10,2,1106,4,10,1,3,1,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,172,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,194,1,103,7,10,1006,0,3,1,4,0,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,228,2,109,0,10,1,101,17,10,1006,0,79,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,260,2,1008,16,10,1,1105,20,10,1,3,17,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,295,1,1002,16,10,101,1,9,9,1007,9,1081,10,1005,10,15,99,109,641,104,0,104,1,21101,387365733012,0,1,21102,1,336,0,1105,1,440,21102,937263735552,1,1,21101,0,347,0,1106,0,440,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,3451034715,1,1,21101,0,394,0,1105,1,440,21102,3224595675,1,1,21101,0,405,0,1106,0,440,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,838337454440,1,21102,428,1,0,1105,1,440,21101,0,825460798308,1,21101,439,0,0,1105,1,440,99,109,2,22101,0,-1,1,21102,1,40,2,21101,0,471,3,21101,461,0,0,1106,0,504,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,466,467,482,4,0,1001,466,1,466,108,4,466,10,1006,10,498,1102,1,0,466,109,-2,2105,1,0,0,109,4,2101,0,-1,503,1207,-3,0,10,1006,10,521,21101,0,0,-3,21202,-3,1,1,22102,1,-2,2,21101,1,0,3,21102,540,1,0,1105,1,545,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,568,2207,-4,-2,10,1006,10,568,22102,1,-4,-4,1106,0,636,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,587,1,0,1105,1,545,21201,1,0,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,606,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,628,22102,1,-1,1,21102,1,628,0,105,1,503,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0
"""