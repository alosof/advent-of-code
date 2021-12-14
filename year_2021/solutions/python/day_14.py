from pathlib import Path
from typing import List, Dict, Tuple

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_lines


def pair_insertion(polymer:str, rules:Dict[str, str], steps:int) -> int:
    chars = count_chars(polymer)
    pairs = count_pairs(polymer)
    for _ in range(steps):
        new_pairs = {}
        for pair in pairs:
            inserted_char = rules[pair]
            chars[inserted_char] = chars.get(inserted_char, 0) + pairs[pair]
            left_pair = pair[0] + inserted_char
            right_pair = inserted_char + pair[1]
            new_pairs[left_pair] = new_pairs.get(left_pair, 0) + pairs[pair]
            new_pairs[right_pair] = new_pairs.get(right_pair, 0) + pairs[pair]
        pairs = new_pairs
    return max(chars.values()) - min(chars.values())


def count_chars(polymer: str) -> Dict[str, int]:
    return {c: polymer.count(c) for c in set(polymer)}


def count_pairs(polymer: str) -> Dict[str, int]:
    return {polymer[i:i+2]: polymer.count(polymer[i:i+2]) for i in range(len(polymer) - 1)}


def read_polymer_and_rules(input_path:Path) -> Tuple[str, Dict[str, str]]:
    lines = read_lines(input_path, str)
    polymer = lines[0]
    rules = {}
    for line in lines[2:]:
        pair, char = line.split(" -> ")
        rules[pair] = char
    return polymer, rules


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    input_polymer, input_rules = read_polymer_and_rules(input_path=input_file_path)

    # Part 1
    part_1_result: int = pair_insertion(polymer=input_polymer, rules=input_rules, steps=10)
    assert part_1_result == 3048
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = pair_insertion(polymer=input_polymer, rules=input_rules, steps=40)
    assert part_2_result == 3288891573057
    print('Part 2 result :', part_2_result)
