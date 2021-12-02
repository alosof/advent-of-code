from pathlib import Path
from typing import List

ROOT_DIRECTORY = Path(__file__).parent.parent.parent.parent
PYTHON_SOLUTIONS_DIRECTORY = ROOT_DIRECTORY / 'solutions' / 'python'
INPUTS_FOLDER = ROOT_DIRECTORY / 'inputs'


def read_lines(input_file_path: Path, line_type: type) -> list:
    with open(input_file_path, 'r') as input_file:
        return [line_type(line) for line in input_file.read().splitlines()]


def read_blocks(input_file_path: Path) -> List[str]:
    with open(input_file_path, 'r') as input_file:
        return [block.replace('\n', ' ') for block in input_file.read().split('\n\n')]


def read_list_of_lists(input_file_path: Path) -> List[List[str]]:
    with open(input_file_path, 'r') as input_file:
        return [block.split('\n') for block in input_file.read().split('\n\n')]


def read_grid(input_file_path: Path) -> List[List[str]]:
    with open(input_file_path, 'r') as input_file:
        return [list(line) for line in input_file.read().split('\n')]
