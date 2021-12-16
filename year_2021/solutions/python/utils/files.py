from pathlib import Path
from typing import List, TypeVar

YEAR_DIRECTORY = Path(__file__).parent.parent.parent.parent
PYTHON_SOLUTIONS_DIRECTORY = YEAR_DIRECTORY / 'solutions' / 'python'
INPUTS_FOLDER = YEAR_DIRECTORY / 'inputs'

T = TypeVar('T', str, int)


def read_lines(input_file_path: Path, line_type: type) -> list:
    with open(input_file_path, 'r') as input_file:
        return [line_type(line) for line in input_file.read().splitlines()]


def read_int_line(input_file_path: Path) -> List[int]:
    with open(input_file_path, 'r') as input_file:
        return [int(e) for e in input_file.read().split(",")]


def read_str(input_file_path: Path) -> str:
    with open(input_file_path, 'r') as input_file:
        return input_file.read()


def read_str_grid(input_file_path: Path) -> List[List[str]]:
    with open(input_file_path, 'r') as input_file:
        return [list(line) for line in input_file.read().split('\n')]


def read_int_grid(input_file_path: Path) -> List[List[int]]:
    with open(input_file_path, 'r') as input_file:
        return [[int(c) for c in line] for line in input_file.read().split('\n')]
