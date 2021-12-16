from math import prod
from operator import gt, lt, eq
from pathlib import Path
from typing import List, Tuple

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_str


def evaluate_expression(hexadecimal: str):
    binary = to_binary(hexadecimal)
    _, value = evaluate(binary)
    return value


def evaluate(binary: str) -> Tuple[str, int]:
    if starts_with_literal(binary):
        literal, _, binary = extract_first_literal_with_version(binary)
        return binary, literal
    else:
        op = get_op(binary)
        subpackets_length_type, subpackets_length_value = get_subpackets_description(binary)
        operands = []
        if subpackets_length_type == "size":
            subpackets_start = 7 + 15
            subpackets_end = subpackets_start + subpackets_length_value
            subpackets = binary[subpackets_start:subpackets_end]
            while len(subpackets) > 0:
                subpackets, element = evaluate(subpackets)
                operands.append(element)
            binary = binary[subpackets_end:]
        else:
            subpackets_start = 7 + 11
            binary = binary[subpackets_start:]
            for i in range(subpackets_length_value):
                binary, element = evaluate(binary)
                operands.append(element)
        return binary, op(operands)


def sum_versions(hexadecimal: str) -> int:
    binary = to_binary(hexadecimal)
    _, collected_versions = collect_versions(binary, [])
    return sum(collected_versions)


def collect_versions(binary: str, collected_versions: List[int]) -> Tuple[str, List[int]]:
    if starts_with_literal(binary):
        _, version, binary = extract_first_literal_with_version(binary)
        collected_versions += [version]
    else:
        version = get_version(binary)
        collected_versions += [version]
        subpackets_length_type, subpackets_length_value = get_subpackets_description(binary)
        if subpackets_length_type == "size":
            subpackets_start = 7 + 15
            subpackets_end = subpackets_start + subpackets_length_value
            subpackets = binary[subpackets_start:subpackets_end]
            while len(subpackets) > 0:
                subpackets, collected_versions = collect_versions(subpackets, collected_versions)
            binary = binary[subpackets_end:]
        else:
            subpackets_start = 7 + 11
            binary = binary[subpackets_start:]
            for i in range(subpackets_length_value):
                binary, collected_versions = collect_versions(binary, collected_versions)
    return binary, collected_versions


def extract_first_literal_with_version(binary: str) -> Tuple[int, int, str]:
    version = get_version(binary)
    literal = ""
    i = 6
    prefix = binary[i]
    while prefix == "1":
        literal += binary[i + 1:i + 5]
        i += 5
        prefix = binary[i]
    literal += binary[i + 1:i + 5]
    binary = binary[i + 5:]
    return to_decimal(literal), version, binary


def starts_with_literal(binary: str) -> bool:
    return get_type_id(binary) == 4


def get_subpackets_description(binary: str) -> Tuple[str, int]:
    length_type_id = binary[6]
    length_type = "size" if length_type_id == "0" else "number"
    length_value = to_decimal(binary[7:7 + 15]) if length_type == "size" else to_decimal(binary[7:7 + 11])
    return length_type, length_value


def get_op(binary: str):
    type_id = get_type_id(binary)
    match type_id:
        case 0:
            return sum
        case 1:
            return prod
        case 2:
            return min
        case 3:
            return max
        case 5:
            return lambda args: gt(*args)
        case 6:
            return lambda args: lt(*args)
        case 7:
            return lambda args: eq(*args)
    pass


def get_type_id(binary):
    return to_decimal(binary[3:6])


def get_version(binary: str) -> int:
    return to_decimal(binary[:3])


def to_decimal(binary: str) -> int:
    return int(binary, base=2)


def to_binary(message: str) -> str:
    translate = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111"
    }
    return "".join([translate[c] for c in message])


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    hexadecimal_transmission: str = read_str(input_file_path)

    # Part 1
    part_1_result: int = sum_versions(hexadecimal_transmission)
    assert part_1_result == 981
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result = evaluate_expression(hexadecimal_transmission)
    assert part_2_result == 299227024091
    print('Part 2 result :', part_2_result)
