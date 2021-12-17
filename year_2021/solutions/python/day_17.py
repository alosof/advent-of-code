from pathlib import Path
from typing import Tuple

from year_2021.solutions.python.utils.files import INPUTS_FOLDER


def highest_peak(tar: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:
    vy_max = 1000
    vx, vy = 1, vy_max
    v = (vx, vy)
    p = (0, 0)
    candidates = []
    while vx < tar[0][1]:
        while vy > 0:
            p, v = step(p, v)
            if out_of_bounds(p, tar):
                vx = vx
                vy = vy - 1
                v = (vx, vy)
                p = (0, 0)
            elif in_bounds(p, tar):
                candidates.append(peak(vy))
        vx += 1
        vy = vy_max
        v = (vx, vy)
        p = (0, 0)
    return max(candidates)


def valid_velocities(tar: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:
    vy_max = 1000
    vx, vy = 1, vy_max
    v = (vx, vy)
    p = (0, 0)
    candidates = []
    while vx <= tar[0][1]:
        while vy >= min(tar[1]):
            p, v = step(p, v)
            if out_of_bounds(p, tar):
                vx = vx
                vy = vy - 1
                v = (vx, vy)
                p = (0, 0)
            elif in_bounds(p, tar):
                if (vx, vy) not in candidates:
                    candidates.append((vx, vy))
        vx += 1
        vy = vy_max
        v = (vx, vy)
        p = (0, 0)
    return len(candidates)


def step(pos: Tuple[int, int], v: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    x, y = pos
    vx, vy = v
    end = (x + vx, y + vy)
    new_v = (int((vx / abs(vx)) * (abs(vx) - 1)) if vx != 0 else 0, vy - 1)
    return end, new_v


def peak(vy: int) -> int:
    return vy * (vy + 1) // 2


def in_bounds(pos: Tuple[int, int], tar: Tuple[Tuple[int, int], Tuple[int, int]]) -> bool:
    x, y = pos
    tar_x, tar_y = tar
    x_min, x_max = tar_x
    y_min, y_max = tar_y
    return x_min <= x <= x_max and y_min <= y <= y_max


def out_of_bounds(pos: Tuple[int, int], tar: Tuple[Tuple[int, int], Tuple[int, int]]) -> bool:
    x, y = pos
    tar_x, tar_y = tar
    x_min, x_max = tar_x
    y_min, y_max = tar_y
    return x > x_max or y < y_min


def read_target_zone(input_path: Path) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    with open(input_path, 'r') as f:
        content = f.read()
    x_range, y_range = content.split(': ')[-1].split(', ')
    x_min, x_max = map(int, x_range.split('=')[-1].split('..'))
    y_min, y_max = map(int, y_range.split('=')[-1].split('..'))
    return (x_min, x_max), (y_min, y_max)


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    target_zone: Tuple[Tuple[int, int], Tuple[int, int]] = read_target_zone(input_path=input_file_path)

    # Part 1
    part_1_result: int = highest_peak(target_zone)
    assert part_1_result == 5565
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result = valid_velocities(target_zone)
    assert part_2_result == 2118
    print('Part 2 result :', part_2_result)
