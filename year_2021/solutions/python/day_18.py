from functools import reduce
from math import ceil, floor
from pathlib import Path
from typing import List

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_lines


def total_sum_magnitude(numbers: List[str]) -> int:
    return magnitude(reduce(add, numbers))


def highest_pair_magnitude(numbers: List[str]) -> int:
    return max(magnitude(add(a, b)) for a in numbers for b in numbers)


def split(regular_number: int) -> str:
    return f"[{floor(regular_number / 2)},{str(ceil(regular_number / 2))}]"


def split_first(snail_number: str) -> str:
    i = 0
    acc = ""
    while i < len(snail_number):
        if snail_number[i] in ['[', ']', ',']:
            if len(acc) > 1:
                break
            acc = ""
        else:
            acc = acc + snail_number[i]
        i += 1
    if i == len(snail_number):
        return snail_number
    else:
        left_part = snail_number[:i - len(acc)]
        right_part = snail_number[i:]
        return left_part + split(int(snail_number[i - len(acc):i])) + right_part


def explode_first(snail_number: str) -> str:
    open_brackets = 0
    i = 0
    while open_brackets < 5 and i < len(snail_number):
        if snail_number[i] == '[':
            open_brackets += 1
        elif snail_number[i] == ']':
            open_brackets -= 1
        i += 1
    if i == len(snail_number):
        return snail_number
    else:
        left_start = i
        left_end = i
        while snail_number[left_end] != ',':
            left_end += 1
        right_start = left_end + 1
        right_end = right_start
        while snail_number[right_end] != ']':
            right_end += 1

        left = snail_number[left_start:left_end]
        right = snail_number[right_start:right_end]

        left_part = ""
        right_part = ""
        acc = ""
        last_unchanged_left = left_start - 1
        for j in range(last_unchanged_left, -1, -1):
            last_unchanged_left = j
            if snail_number[j] in ['[', ']', ',']:
                if len(acc) > 0:
                    left_part = str(int(acc) + int(left)) + left_part
                    left_part = snail_number[j] + left_part
                    break
                left_part = snail_number[j] + left_part
                acc = ""
            else:
                acc = snail_number[j] + acc
        left_part = snail_number[:last_unchanged_left] + left_part
        acc = ""
        first_unchanged_right = right_end
        for k in range(first_unchanged_right, len(snail_number)):
            first_unchanged_right = k
            if snail_number[k] in ['[', ']', ',']:
                if len(acc) > 0:
                    right_part = right_part + str(int(acc) + int(right))
                    right_part = right_part + snail_number[k]
                    break
                right_part = right_part + snail_number[k]
                acc = ""
            else:
                acc = acc + snail_number[k]
        right_part = right_part + snail_number[first_unchanged_right + 1:]
        return left_part[:-1] + "0" + right_part[1:]


def reduce_snail(snail_number: str) -> str:
    new_n = explode_first(snail_number)
    if new_n == snail_number:
        new_n = split_first(snail_number)
        if new_n == snail_number:
            return new_n
    return reduce_snail(new_n)


def add(a: str, b: str) -> str:
    return reduce_snail(f"[{a},{b}]")


def magnitude(snail_number: str) -> int:
    eval_snail_number = eval(str(snail_number))
    if all([isinstance(e, int) for e in eval_snail_number]):
        return 3 * eval_snail_number[0] + 2 * eval_snail_number[1]
    elif isinstance(eval_snail_number[0], int):
        return 3 * eval_snail_number[0] + 2 * magnitude(eval_snail_number[1])
    elif isinstance(eval_snail_number[1], int):
        return 3 * magnitude(eval_snail_number[0]) + 2 * eval_snail_number[1]
    else:
        return 3 * magnitude(eval_snail_number[0]) + 2 * magnitude(eval_snail_number[1])


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    snail_numbers: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = total_sum_magnitude(snail_numbers)
    assert part_1_result == 3675
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result = highest_pair_magnitude(snail_numbers)
    assert part_2_result == 4650
    print('Part 2 result :', part_2_result)
