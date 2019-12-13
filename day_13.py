from collections import defaultdict
from enum import IntEnum
from typing import Dict, List, Tuple

from computer import IntCodeComputer, IO, scan_program_from_input
from mapping import C2


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class Screen(object):
    pixels: Dict[C2, Tile]

    def __init__(self):
        self.pixels = defaultdict(lambda: Tile.EMPTY)

    def count_blocks(self) -> int:
        total = 0
        for value in self.pixels.values():
            if value == Tile.BLOCK:
                total += 1
        return total

    def get_ball_and_paddle_positions(self) -> Dict[str, C2]:
        paddle = None
        ball = None
        for cord, tile in self.pixels.items():
            if tile == Tile.PADDLE:
                paddle = cord
            if tile == Tile.BALL:
                ball = cord
            if ball is not None and paddle is not None:
                break
        return {
            "ball": ball,
            "paddle": paddle
        }

    def print(self):
        min_x = 99999999
        min_y = 99999999
        max_x = -99999999
        max_y = -99999999
        for cord, tile in self.pixels.items():
            if cord.x < min_x:
                min_x = cord.x
            if cord.x > max_x:
                max_x = cord.x
            if cord.y < min_y:
                min_y = cord.y
            if cord.y > max_y:
                max_y = cord.y
        for h in range(min_y, max_y + 1):
            line = ""
            for w in range(min_x, max_x + 1):
                t = self.pixels[C2(w, h)]
                if t == Tile.EMPTY:
                    line += " "
                elif t == Tile.BLOCK:
                    line += "#"
                elif t == Tile.BALL:
                    line += "o"
                elif t == Tile.PADDLE:
                    line += "_"
                elif t == Tile.WALL:
                    line += "|"
            print(line)


class ArcadeIO(IO):
    screen: Screen
    stdout: List[str]

    def __init__(self, screen: Screen):
        self.screen = screen
        self.stdout = []

    def input(self) -> str:
        self.screen.print()
        info = self.screen.get_ball_and_paddle_positions()

        ball = info["ball"]
        paddle = info["paddle"]

        if ball is None or paddle is None:
            return "0"

        if ball.x > paddle.x:
            return "1"
        elif ball.x < paddle.x:
            return "-1"
        return "0"

    def output(self, out: str) -> None:
        self.stdout.append(out)

        if len(self.stdout) == 3:
            x = int(self.stdout[0])
            y = int(self.stdout[1])

            if x == -1 and y == 0:
                print("score:", int(self.stdout[2]))
            else:
                tile = Tile(int(self.stdout[2]))

                self.screen.pixels[C2(x, y)] = tile

            self.stdout = []


def main():
    screen = Screen()
    cpu = IntCodeComputer(scan_program_from_input(),
                          ArcadeIO(screen))
    cpu.hard_set_memory_cell(0, 2)

    cpu.run()
    # print(screen.count_blocks())


if __name__ == '__main__':
    main()

"""
1,380,379,385,1008,2159,116649,381,1005,381,12,99,109,2160,1101,0,0,383,1101,0,0,382,21001,382,0,1,21001,383,0,2,21102,1,37,0,1106,0,578,4,382,4,383,204,1,1001,382,1,382,1007,382,38,381,1005,381,22,1001,383,1,383,1007,383,20,381,1005,381,18,1006,385,69,99,104,-1,104,0,4,386,3,384,1007,384,0,381,1005,381,94,107,0,384,381,1005,381,108,1105,1,161,107,1,392,381,1006,381,161,1102,-1,1,384,1105,1,119,1007,392,36,381,1006,381,161,1102,1,1,384,21002,392,1,1,21101,0,18,2,21102,1,0,3,21101,0,138,0,1106,0,549,1,392,384,392,20102,1,392,1,21102,18,1,2,21102,3,1,3,21101,0,161,0,1105,1,549,1101,0,0,384,20001,388,390,1,21002,389,1,2,21101,180,0,0,1106,0,578,1206,1,213,1208,1,2,381,1006,381,205,20001,388,390,1,21002,389,1,2,21101,0,205,0,1106,0,393,1002,390,-1,390,1102,1,1,384,21001,388,0,1,20001,389,391,2,21102,228,1,0,1105,1,578,1206,1,261,1208,1,2,381,1006,381,253,20102,1,388,1,20001,389,391,2,21101,253,0,0,1105,1,393,1002,391,-1,391,1102,1,1,384,1005,384,161,20001,388,390,1,20001,389,391,2,21102,1,279,0,1106,0,578,1206,1,316,1208,1,2,381,1006,381,304,20001,388,390,1,20001,389,391,2,21102,304,1,0,1105,1,393,1002,390,-1,390,1002,391,-1,391,1102,1,1,384,1005,384,161,20101,0,388,1,20101,0,389,2,21102,0,1,3,21102,338,1,0,1106,0,549,1,388,390,388,1,389,391,389,20101,0,388,1,21001,389,0,2,21101,0,4,3,21101,0,365,0,1105,1,549,1007,389,19,381,1005,381,75,104,-1,104,0,104,0,99,0,1,0,0,0,0,0,0,280,17,15,1,1,19,109,3,21201,-2,0,1,22101,0,-1,2,21102,0,1,3,21102,414,1,0,1106,0,549,21202,-2,1,1,21202,-1,1,2,21102,429,1,0,1105,1,601,2101,0,1,435,1,386,0,386,104,-1,104,0,4,386,1001,387,-1,387,1005,387,451,99,109,-3,2105,1,0,109,8,22202,-7,-6,-3,22201,-3,-5,-3,21202,-4,64,-2,2207,-3,-2,381,1005,381,492,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,481,21202,-4,8,-2,2207,-3,-2,381,1005,381,518,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,507,2207,-3,-4,381,1005,381,540,21202,-4,-1,-1,22201,-3,-1,-3,2207,-3,-4,381,1006,381,529,21202,-3,1,-7,109,-8,2105,1,0,109,4,1202,-2,38,566,201,-3,566,566,101,639,566,566,1202,-1,1,0,204,-3,204,-2,204,-1,109,-4,2106,0,0,109,3,1202,-1,38,594,201,-2,594,594,101,639,594,594,20101,0,0,-2,109,-3,2105,1,0,109,3,22102,20,-2,1,22201,1,-1,1,21102,1,383,2,21101,430,0,3,21102,1,760,4,21101,0,630,0,1105,1,456,21201,1,1399,-2,109,-3,2106,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,2,2,2,0,2,2,2,0,0,2,2,2,0,2,0,2,2,0,2,2,2,2,2,0,2,2,2,0,0,0,0,0,1,1,0,0,2,2,2,2,2,2,2,2,0,2,2,0,0,2,2,0,0,2,2,2,2,0,0,0,0,0,2,2,2,2,0,0,2,0,1,1,0,0,2,2,2,0,2,2,2,2,2,2,2,0,2,0,2,2,0,0,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,1,1,0,0,0,2,0,2,2,2,0,2,2,2,2,2,2,2,2,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,0,1,1,0,0,2,0,0,2,2,2,0,2,2,2,2,0,2,0,2,0,2,2,2,2,2,2,2,0,0,2,2,2,2,2,0,2,2,0,1,1,0,2,2,0,2,0,2,2,0,2,2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,0,2,2,2,0,2,0,2,0,0,1,1,0,2,2,2,2,2,2,2,2,0,2,0,2,2,2,0,0,0,2,0,2,2,2,0,2,2,2,2,2,0,0,2,2,0,2,0,1,1,0,0,2,2,0,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,0,2,2,2,2,2,2,0,1,1,0,2,0,2,2,2,0,2,2,2,0,0,2,2,2,2,0,0,0,2,2,2,0,0,2,0,0,2,2,2,2,0,2,0,0,0,1,1,0,2,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,2,2,2,2,0,2,2,2,2,2,0,2,0,0,1,1,0,2,2,2,0,2,2,0,0,2,2,2,2,0,0,2,2,2,0,0,2,2,0,2,0,2,0,2,0,2,2,0,2,2,2,0,1,1,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,2,0,0,2,2,2,0,0,2,2,2,0,2,2,2,2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,19,28,61,4,98,57,92,26,50,7,4,93,91,74,82,82,53,50,44,66,37,43,26,12,68,84,76,40,36,22,37,44,27,92,66,68,29,34,45,60,40,21,65,41,40,64,92,11,36,81,37,39,87,7,42,10,72,35,35,51,60,76,47,1,6,51,48,46,18,82,84,11,42,76,65,98,62,71,83,51,79,76,70,46,10,67,87,78,6,63,38,23,97,69,82,84,20,97,83,4,70,96,75,38,33,32,69,80,52,80,91,95,2,30,56,52,49,64,38,32,18,97,82,93,76,1,8,37,42,80,66,38,53,33,1,31,40,54,90,20,78,13,65,4,35,28,67,37,28,56,69,50,89,63,20,55,68,59,90,18,28,25,73,25,39,26,6,65,83,5,14,4,31,9,53,25,2,9,34,10,21,43,23,39,15,29,52,36,10,71,35,18,90,86,53,58,7,10,33,81,5,50,64,17,84,85,17,37,48,43,71,10,13,83,8,88,66,95,42,54,91,62,64,53,58,56,42,67,12,29,34,14,58,37,37,49,42,8,41,44,41,17,62,59,54,67,43,42,65,12,23,76,79,93,12,35,65,87,12,74,28,56,74,25,68,91,69,98,26,67,54,18,25,63,60,28,84,93,93,93,7,84,52,50,7,18,16,57,27,87,61,30,20,81,59,33,98,27,15,83,89,44,26,31,79,3,46,29,24,64,94,58,87,1,87,63,55,68,27,4,98,5,8,30,73,74,30,4,57,78,33,55,1,50,16,87,67,59,62,85,3,2,89,54,44,95,34,8,10,78,75,6,70,53,48,60,68,60,79,4,51,81,66,58,44,45,91,69,24,41,96,6,98,45,87,46,29,83,29,90,13,22,7,83,56,89,62,54,87,32,12,1,78,19,37,66,42,13,49,16,32,90,43,28,72,67,42,18,10,55,27,21,75,95,24,91,9,70,48,5,49,70,11,79,23,24,93,30,21,34,40,56,25,62,55,26,38,74,67,23,33,35,41,83,79,64,61,87,4,29,66,82,67,97,46,78,95,73,15,9,90,19,52,67,66,91,73,97,51,4,35,52,33,86,35,16,45,1,18,23,72,67,94,3,8,67,87,19,10,79,35,24,57,60,21,48,55,37,58,81,95,15,48,70,37,69,92,87,85,6,13,44,21,12,9,14,61,69,18,65,56,50,20,23,23,4,72,30,92,50,91,83,17,94,10,83,21,70,50,65,20,39,70,7,61,34,57,38,38,39,55,48,68,56,24,66,18,41,60,25,56,50,43,65,61,95,25,30,95,10,51,31,41,64,52,5,21,37,62,75,55,10,96,28,85,12,28,4,86,46,14,26,48,26,77,15,69,16,58,68,91,32,5,66,53,69,48,54,38,13,10,9,18,67,45,97,65,74,72,7,47,93,79,77,87,68,80,8,53,86,77,33,74,78,94,92,22,9,41,34,76,25,66,55,53,1,62,23,82,23,70,58,43,34,16,6,15,55,7,5,51,23,14,11,94,91,40,21,18,28,1,77,86,27,97,6,7,31,58,20,64,41,16,65,8,11,6,51,48,44,81,5,78,18,27,89,24,55,97,70,83,48,37,97,77,32,41,80,30,25,63,76,75,85,84,61,65,13,82,69,41,28,9,46,57,60,71,55,70,13,26,90,20,21,29,59,80,60,33,73,14,19,83,12,35,52,51,70,79,36,36,40,55,31,80,43,76,59,33,82,116649
"""