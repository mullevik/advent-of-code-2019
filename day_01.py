import fileinput


def calculate_fuel(mass: int) -> int:
    return (mass // 3) - 2


if __name__ == "__main__":
    total_fuel_requirement = 0

    for line in fileinput.input():
        module_mass = int(line)

        fuel_requirements = []
        fuel_requirement = calculate_fuel(module_mass)
        while fuel_requirement > 0:
            fuel_requirements.append(fuel_requirement)
            fuel_requirement = calculate_fuel(fuel_requirement)

        total_fuel_requirement += sum(fuel_requirements)

    print(total_fuel_requirement)
