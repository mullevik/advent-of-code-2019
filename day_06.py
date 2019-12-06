from typing import Dict, List


def bfs(start: str, end: str, graph: Dict[str, List[str]]) -> int:
    queue: List[str] = [start]

    visited = set()

    distances = {}
    for node in graph.keys():
        distances[node] = 0

    while queue:
        current = queue.pop(0)

        for child in graph[current]:

            if child not in visited:
                visited.add(child)
                queue.append(child)
                distances[child] = distances[current] + 1

                if child == end:
                    return distances[end]

    raise ValueError("End not found")


def count_orbits_for_planet(node: str, graph: Dict[str, List[str]]) -> int:
    stack: List[str] = [node]
    visited = set()

    orbits = 0

    while stack:
        current = stack.pop()

        for child in graph[current]:

            # if child not in visited:
            orbits += 1
            stack.append(child)

    return orbits


def count_orbits(graph: Dict[str, List[str]]) -> int:

    total_number_of_orbits = 0

    for node in graph.keys():
        total_number_of_orbits += count_orbits_for_planet(node, graph)

    return total_number_of_orbits


def main():
    graph = {}

    while True:
        input_string = input()

        if input_string == "":
            break

        input_list = input_string.split(")")

        parent = input_list[0]
        child = input_list[1]

        if child not in graph:
            graph[child] = []
        if parent not in graph:
            graph[parent] = []

        # make undirected edge
        graph[parent].append(child)
        graph[child].append(parent)

    number_of_jumps = bfs("YOU", "SAN", graph) - 2

    print(number_of_jumps)


if __name__ == "__main__":
    main()
