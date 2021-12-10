from functools import reduce
from pathlib import Path
from statistics import median
from typing import List

from year_2021.solutions.python.utils.files import INPUTS_FOLDER, read_lines


def autocomplete_score(lines: List[str]) -> int:
    return median(autocomplete_line_score(line) for line in lines if is_incomplete(line))


def autocomplete_line_score(incomplete_line: str) -> int:
    openers = []
    for c in incomplete_line:
        if c in ['(', '[', '{', '<']:
            openers.append(c)
        else:
            openers.pop()
    return reduce(lambda x, y: 5 * x + y, [0] + [legal_closing_score(opposite(o)) for o in reversed(openers)])


def syntax_error_score(lines: List[str]) -> int:
    return sum(syntax_error_line_score(line) for line in lines)


def syntax_error_line_score(line: str) -> int:
    openers = []
    for c in line:
        if c in ['(', '[', '{', '<']:
            openers.append(c)
        else:
            last_opener = openers.pop()
            if opposite(last_opener) != c:
                return illegal_closing_score(c)
    return 0


def is_incomplete(line: str) -> bool:
    return syntax_error_line_score(line) == 0


def legal_closing_score(character: str) -> int:
    if character == ')':
        return 1
    elif character == ']':
        return 2
    elif character == '}':
        return 3
    elif character == '>':
        return 4


def illegal_closing_score(character: str) -> int:
    if character == ')':
        return 3
    elif character == ']':
        return 57
    elif character == '}':
        return 1197
    elif character == '>':
        return 25137


def opposite(character: str) -> str:
    if character == '(':
        return ')'
    elif character == '[':
        return ']'
    elif character == '{':
        return '}'
    elif character == '<':
        return '>'
    elif character == ')':
        return '('
    elif character == ']':
        return '['
    elif character == '}':
        return '{'
    elif character == '>':
        return '<'


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    input_lines: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = syntax_error_score(lines=input_lines)
    assert part_1_result == 294195
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = autocomplete_score(lines=input_lines)
    assert part_2_result == 3490802734
    print('Part 2 result :', part_2_result)
