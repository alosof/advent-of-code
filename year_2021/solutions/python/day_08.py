from pathlib import Path
from typing import List, Dict

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_lines


def count_easy_digits(entries: List[List[List[str]]]) -> int:
    return sum(len(pattern) in [2, 3, 4, 7] for entry in entries for pattern in entry[1])


def sum_decoded_outputs(entries: List[List[List[str]]]) -> int:
    return sum(decode(entry[1], entry[0]) for entry in entries)


def normalize_pattern(pattern: str) -> str:
    return ''.join(sorted(pattern))


def decode(four_digit_encoding: List[str], unique_signal_patterns: List[str]) -> int:
    decoding_map = build_decoding_map(unique_signal_patterns)
    return int(''.join([str(decoding_map[normalize_pattern(pattern)]) for pattern in four_digit_encoding]))


def build_decoding_map(unique_signal_patterns: List[str]) -> Dict[str, int]:
    decoding_map: Dict[str, int] = {}
    for pattern in unique_signal_patterns:
        if len(pattern) == 2:
            decoding_map[normalize_pattern(pattern)] = 1
        elif len(pattern) == 3:
            decoding_map[normalize_pattern(pattern)] = 7
        elif len(pattern) == 4:
            decoding_map[normalize_pattern(pattern)] = 4
        elif len(pattern) == 7:
            decoding_map[normalize_pattern(pattern)] = 8

    easy_digits_encoding_map: Dict[int, str] = {digit: code for (code, digit) in decoding_map.items()}
    for pattern in unique_signal_patterns:
        normalized_pattern = normalize_pattern(pattern)
        if normalized_pattern not in decoding_map:
            decoding_map[normalized_pattern] = guess_difficult_digit(normalized_pattern, easy_digits_encoding_map)

    return decoding_map


def guess_difficult_digit(normalized_pattern: str, easy_digits_encoding_map: Dict[int, str]) -> int:
    if (len(set(normalized_pattern).intersection(easy_digits_encoding_map[8])) == 6 and
        len(set(normalized_pattern).intersection(easy_digits_encoding_map[4])) == 4):
        return 9
    elif (len(set(normalized_pattern).intersection(easy_digits_encoding_map[8])) == 6 and
          len(set(normalized_pattern).intersection(easy_digits_encoding_map[1])) == 1):
        return 6
    elif len(set(normalized_pattern).intersection(easy_digits_encoding_map[8])) == 6:
        return 0
    elif len(set(normalized_pattern).intersection(easy_digits_encoding_map[1])) == 2:
        return 3
    elif len(set(normalized_pattern).intersection(easy_digits_encoding_map[4])) == 3:
        return 5
    else:
        return 2


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    note_entries: List[List[List[str]]] = [
        [part.split() for part in line.split(' | ')]
        for line in read_lines(input_file_path=input_file_path, line_type=str)
    ]

    # Part 1
    part_1_result: int = count_easy_digits(note_entries)
    assert part_1_result == 548
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = sum_decoded_outputs(note_entries)
    assert part_2_result == 1074888
    print('Part 2 result :', part_2_result)
