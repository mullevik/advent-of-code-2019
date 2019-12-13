from typing import NamedTuple, List, Tuple


class Vec3(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other) -> 'Vec3':
        if not isinstance(other, Vec3):
            raise TypeError("Unsupported operation")
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)


class Moon(object):
    position: Vec3
    velocity: Vec3

    def __init__(self, position: Vec3):
        self.position = position
        self.velocity = Vec3(0, 0, 0)

    def update_velocity(self, new_velocity: Vec3):
        self.velocity = self.velocity + new_velocity

    def apply_velocity(self):
        self.position = self.position + self.velocity

    def kinetic_energy(self) -> int:
        return abs(self.velocity.x) + abs(self.velocity.y) \
               + abs(self.velocity.z)

    def potential_energy(self) -> int:
        return abs(self.position.x) + abs(self.position.y) \
               + abs(self.position.z)


class Map(object):
    moons: List[Moon]

    def __init__(self, moons: List[Moon]):
        self.moons = moons

    def add_moon(self, moon: Moon):
        self.moons.append(moon)

    def apply_gravity(self):
        for first in self.moons:
            dx = 0
            dy = 0
            dz = 0

            for second in self.moons:
                if first.position.x < second.position.x:
                    dx += 1
                elif first.position.x > second.position.x:
                    dx += -1
                if first.position.y < second.position.y:
                    dy += 1
                elif first.position.y > second.position.y:
                    dy += -1
                if first.position.z < second.position.z:
                    dz += 1
                elif first.position.z > second.position.z:
                    dz += -1
            first.update_velocity(Vec3(dx, dy, dz))

    def apply_changes(self):
        for moon in self.moons:
            moon.apply_velocity()

    def calculate_energy(self) -> int:
        total = 0
        for moon in self.moons:
            total += moon.kinetic_energy() * moon.potential_energy()
        return total


def parse_input_line(line: str) -> Moon:
    filtered_line = line.replace("<", "").replace(">", "").replace("x=", "") \
        .replace("y=", "").replace("z=", "")

    coordinates = filtered_line.split(",")
    pos = Vec3(int(coordinates[0]), int(coordinates[1]), int(coordinates[2]))
    return Moon(pos)


def parse_input() -> List[Moon]:
    moons = []
    while True:
        line = input()
        if line == "":
            break
        moons.append(parse_input_line(line))
    return moons


def states_equal(orig_pos: List[Vec3], orig_vel: List[Vec3],
                 moons: List[Moon]) -> bool:
    for i in range(len(moons)):
        if orig_pos[i] != moons[i].position:
            return False
        if orig_vel[i] != moons[i].velocity:
            return False
    return True


def main():
    m = Map(parse_input())

    original_positions = []
    original_velocities = []
    for moon in m.moons:
        original_positions.append(moon.position)
        original_velocities.append(moon.velocity)

    last_time = 1000000000000

    time = 0
    while time < last_time:
        time += 1
        print(time)
        m.apply_gravity()
        m.apply_changes()

        if states_equal(original_positions, original_velocities, m.moons):
            break

    print(m.calculate_energy())


if __name__ == '__main__':
    main()

"""
<x=-16, y=15, z=-9>
<x=-14, y=5, z=4>
<x=2, y=0, z=6>
<x=-3, y=18, z=9>
"""