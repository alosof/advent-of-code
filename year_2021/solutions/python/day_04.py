from pathlib import Path
from typing import List, Tuple, Dict

from year_2021.solutions.python.utils.files import INPUTS_FOLDER


def find_first_winning_board_score(bingo: List[int], boards: Dict[int, List[List[int]]]) -> int:
    for number in bingo:
        for i in boards:
            boards[i] = mark_number(number, boards[i])
            if has_complete_line(boards[i]):
                return number * sum_unmarked_numbers(boards[i])


def find_last_winning_board_score(bingo: List[int], boards: Dict[int, List[List[int]]]) -> int:
    done_boards = set()
    for number in bingo:
        for i in boards:
            if i not in done_boards:
                boards[i] = mark_number(number, boards[i])
                if has_complete_line(boards[i]):
                    done_boards.add(i)
                    if len(done_boards) == len(boards):
                        return number * sum_unmarked_numbers(boards[i])


def sum_unmarked_numbers(board: List[List[int]]) -> int:
    return sum((e for row in board for e in row if e != -1))


def mark_number(number: int, board: List[List[int]]) -> List[List[int]]:
    return [[(-1 if e == number else e) for e in row] for row in board]


def has_complete_line(board: List[List[int]]) -> bool:
    return has_complete_row(board) or has_complete_column(board)


def has_complete_column(board: List[List[int]]) -> bool:
    return has_complete_row(transpose(board))


def has_complete_row(board: List[List[int]]) -> bool:
    return any(all(e == -1 for e in row) for row in board)


def transpose(board: List[List[int]]) -> List[List[int]]:
    n_columns = len(board[0])
    return [[row[c] for row in board] for c in range(n_columns)]


def read_bingo_and_boards(file_path: Path) -> Tuple[List[int],
                                                    Dict[int, List[List[int]]]]:
    with open(file_path, 'r') as input_file:
        file_content = input_file.read()
        blocks = file_content.split('\n\n')
        bingo = [int(n) for n in blocks[0].split(',')]
        boards = {}
        for i, block in enumerate(blocks[1:]):
            boards[i] = [[int(n) for n in row.split()] for row in block.split('\n')]
        return bingo, boards


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    bingo_, boards_ = read_bingo_and_boards(file_path=input_file_path)

    # Part 1
    part_1_result: int = find_first_winning_board_score(bingo_, boards_)
    assert part_1_result == 63552
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = find_last_winning_board_score(bingo_, boards_)
    assert part_2_result == 9020
    print('Part 2 result :', part_2_result)
