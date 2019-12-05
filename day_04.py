from typing import List, Tuple, NamedTuple


def is_six_digit(digits: str):
    return len(digits) == 6


def has_two_adjacent_same_digits(digits: str):
    for i in range(len(digits) - 1):
        if digits[i] == digits[i + 1]:
            return True
    return False


def has_increasing_digits_only(digits: str):
    previous = 0
    for char in digits:
        int_digit = int(char)
        if int_digit < previous:
            return False
        else:
            previous = int_digit
    return True


def has_exactly_one_double_digit(digits: str):
    custom_representation = "x" + digits + "x"
    for i in range(len(digits) - 1):
        digit_1 = custom_representation[i]
        digit_2 = custom_representation[i + 1]
        digit_3 = custom_representation[i + 2]
        digit_4 = custom_representation[i + 3]

        if digit_2 == digit_3 and digit_2 != digit_1 and digit_2 != digit_4:
            return True

    return False


if __name__ == "__main__":
    number_of_possible_passwords = 0
    for number in range(240920, 789857 + 1, 1):
        str_representation = str(number)

        if has_two_adjacent_same_digits(str_representation) \
                and has_increasing_digits_only(str_representation)\
                and has_exactly_one_double_digit(str_representation):
            print(number)
            number_of_possible_passwords += 1

    print("number of passwords: {}".format(number_of_possible_passwords))




