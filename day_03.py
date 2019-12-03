from typing import List, Tuple, NamedTuple


class Position(NamedTuple):
    x: int
    y: int
    steps: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


def trace_line(source: Position, destination: Position) -> List[Position]:
    """Excludes the source position."""
    traced_positions = []

    if source.x == destination.x:
        step_direction = 1
        if source.y > destination.y:
            step_direction = -1

        t = 1
        for i in range(source.y + step_direction,
                       destination.y + step_direction,
                       step_direction):
            traced_positions.append(Position(x=source.x, y=i,
                                             steps=source.steps + t))
            t += 1

    elif source.y == destination.y:
        step_direction = 1
        if source.x > destination.x:
            step_direction = -1

        t = 1
        for i in range(source.x + step_direction,
                       destination.x + step_direction,
                       step_direction):
            traced_positions.append(Position(x=i, y=source.y,
                                             steps=source.steps + t))
            t += 1

    else:
        raise ValueError("Not a straight line")

    return traced_positions


def trace_poly_line(positions: List[Position]) -> List[Position]:
    traced_positions = []
    current = positions[0]

    for position in positions:
        traced_positions += trace_line(current, position)
        current = position

    return traced_positions


def trace_commands(command_sequence: List[str]) -> List[Position]:
    current_position = Position(x=0, y=0, steps=0)

    all_positions = [current_position]

    for command in command_sequence:
        direction = command[0]
        step_size = int(command[1:])
        if direction == "R":
            current_position = Position(x=current_position.x + step_size,
                                        y=current_position.y,
                                        steps=current_position.steps + step_size)
        elif direction == "L":
            current_position = Position(x=current_position.x - step_size,
                                        y=current_position.y,
                                        steps=current_position.steps + step_size)
        elif direction == "U":
            current_position = Position(x=current_position.x,
                                        y=current_position.y + step_size,
                                        steps=current_position.steps + step_size)
        elif direction == "D":
            current_position = Position(x=current_position.x,
                                        y=current_position.y - step_size,
                                        steps=current_position.steps + step_size)
        all_positions.append(current_position)

    return trace_poly_line(all_positions)


def distance(pos: Position) -> int:
    return abs(pos.x) + abs(pos.y)


if __name__ == "__main__":
    input_string = input()
    first_commands = input_string.split(",")
    first_trace = trace_commands(first_commands)
    first_trace_set = set(first_trace)

    first_dict = {pos: pos.steps for pos in first_trace_set}

    input_string = input()
    second_commands = input_string.split(",")
    second_trace = trace_commands(second_commands)

    second_trace_set = set(second_trace)

    second_dict = {pos: pos.steps for pos in second_trace_set}

    intersection = first_trace_set.intersection(second_trace_set)

    minimal_number_of_steps = len(first_trace) + len(second_trace)

    for position in intersection:
        step_sum = first_dict[position] + second_dict[position]
        if step_sum < minimal_number_of_steps:
            minimal_number_of_steps = step_sum

    print(minimal_number_of_steps)

