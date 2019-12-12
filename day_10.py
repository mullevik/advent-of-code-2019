from typing import NamedTuple, Dict, List
import math

class Pos(NamedTuple):
    x: int
    y: int


class Data(object):
    is_asteroid: bool
    is_bfs_visited: bool
    is_reachable: bool

    def __init__(self, raw_input: chr):
        if raw_input == ".":
            self.is_asteroid = False
        else:
            self.is_asteroid = True
        self.is_bfs_visited = False
        self.is_reachable = True

    def visit(self):
        self.is_bfs_visited = True

    def burn(self):
        self.is_reachable = False


class Map(object):
    width: int
    height: int
    map: Dict[Pos, Data]
    source: Pos

    def __init__(self, width: int, height: int, raw_input: List[str],
                 source: Pos):
        self.width = width
        self.height = height

        self.map = {}
        for h_index, line in enumerate(raw_input):
            for w_index, char in enumerate(line):
                self.map[Pos(w_index, h_index)] = Data(char)

        if not self.map[source].is_asteroid:
            raise ValueError("source must be asteroid")
        self.source = source

    def contains(self, pos: Pos) -> bool:
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            return True
        return False

    @staticmethod
    def _all_adjacent(pos: Pos) -> List[Pos]:
        positions = []
        for x in range(pos.x - 1, pos.x + 2, 1):
            for y in range(pos.y - 1, pos.y + 2, 1):
                adjacent = Pos(x, y)
                if adjacent != pos:
                    positions.append(adjacent)
        return positions

    def adjacent(self, pos: Pos) -> List[Pos]:
        all_adjacent = self._all_adjacent(pos)
        positions = []
        for adjacent in all_adjacent:
            if self.contains(adjacent):
                positions.append(adjacent)
        return positions

    def difference(self, to: Pos) -> Pos:
        difference = Pos(x=to.x - self.source.x, y=to.y - self.source.y)
        divider = math.gcd(difference.x, difference.y)

        difference = Pos(difference.x / divider, difference.y / divider)
        return difference

    def burn(self, difference: Pos):
        current = Pos(self.source.x + difference.x,
                      self.source.y + difference.y)
        while self.contains(current):
            self.map[current].burn()
            current = Pos(current.x + difference.x, current.y + difference.y)

    def remove_asteroids(self, asteroids: List[Pos]):
        for asteroid in asteroids:
            self.map[asteroid].is_asteroid = False

    def visible_asteroids(self) -> List[Pos]:

        self.map[self.source].visit()
        bfs_queue = [self.source]

        visible_asteroids = []

        while bfs_queue:
            current = bfs_queue.pop(0)

            for adjacent in self.adjacent(current):
                adjacent_data = self.map[adjacent]

                if not adjacent_data.is_bfs_visited:
                    adjacent_data.visit()
                    bfs_queue.append(adjacent)

                    if adjacent_data.is_reachable \
                            and adjacent_data.is_asteroid:
                        visible_asteroids.append(adjacent)
                        difference = self.difference(adjacent)
                        self.burn(difference)

        return visible_asteroids


def main():
    raw_input = []

    while True:
        line = input()

        if line == "":
            break
        raw_input.append(line)

    width = len(raw_input[0])
    height = len(raw_input)

    source = Pos(11, 19)

    def angle(pos: Pos):
        in_source = source

        dx = pos.x - in_source.x
        dy = in_source.y - pos.y

        if dx >= 0 and dy > 0:
            rad_ang = math.atan(dx / dy)
        elif dx > 0 and dy <= 0:
            rad_ang = math.atan(- dy / dx) + (math.pi / 2)
        elif dx <= 0 and dy < 0:
            rad_ang = math.atan(- dx / dy) + math.pi
        elif dx < 0 and dy >= 0:
            rad_ang = math.atan(dy / -dx) + (3 / 2) * math.pi
        else:
            rad_ang = 0.
        # print(math.degrees(rad_ang))
        return rad_ang

    all_asteroids = []
    index = 0
    while True:
        m = Map(width, height, raw_input, source)
        m.remove_asteroids(all_asteroids)
        asteroids = m.visible_asteroids()
        all_asteroids += asteroids

        if len(all_asteroids) >= 200:
            asteroids.sort(key=lambda x: angle(x))
            the_asteroid = asteroids[199 - index]
            break
        else:
            index = len(all_asteroids)

    print(the_asteroid)

if __name__ == '__main__':
    main()

"""
.#..#
.....
#####
....#
...##

.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

"""
Position 11,19 is the argmax for part 1
"""