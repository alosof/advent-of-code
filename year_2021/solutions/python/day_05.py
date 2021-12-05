from dataclasses import dataclass
from pathlib import Path
from typing import List

from year_2021.solutions.python.utils.files import INPUTS_FOLDER


def count_segment_overlaps(segments: List['Segment'], use_diagonals: bool) -> int:
    visits_counts = {}
    for segment in segments:
        if not use_diagonals and segment.direction == 'd':
            continue
        for point in segment.get_points():
            if point in visits_counts:
                visits_counts[point] += 1
            else:
                visits_counts[point] = 1
    return len([point for point, visits in visits_counts.items() if visits > 1])


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Segment:

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        if self.start.y == self.end.y:
            self.direction = 'h'
        elif self.start.x == self.end.x:
            self.direction = 'v'
        elif abs(self.end.x - self.start.x) == abs(self.end.y - self.start.y):
            self.direction = 'd'
        else:
            raise ValueError('Invalid segment. Each segment should be either horizontal, vertical or diagonal.')

    def get_points(self) -> List[Point]:
        match self.direction, self.is_increasing('x'), self.is_increasing('y'):
            case 'h', True, _:
                return [Point(x, self.start.y) for x in range(self.start.x, self.end.x + 1)]
            case 'h', False, _:
                return [Point(x, self.start.y) for x in range(self.start.x, self.end.x - 1, -1)]
            case 'v', _, True:
                return [Point(self.start.x, y) for y in range(self.start.y, self.end.y + 1)]
            case 'v', _, False:
                return [Point(self.start.x, y) for y in range(self.start.y, self.end.y - 1, -1)]
            case 'd', True, True:
                return [Point(x, y)
                        for x, y in zip(range(self.start.x, self.end.x + 1), range(self.start.y, self.end.y + 1))]
            case 'd', True, False:
                return [Point(x, y)
                        for x, y in zip(range(self.start.x, self.end.x + 1), range(self.start.y, self.end.y - 1, -1))]
            case 'd', False, True:
                return [Point(x, y)
                        for x, y in zip(range(self.start.x, self.end.x - 1, -1), range(self.start.y, self.end.y + 1))]
            case 'd', False, False:
                return [Point(x, y)
                        for x, y in
                        zip(range(self.start.x, self.end.x - 1, -1), range(self.start.y, self.end.y - 1, -1))]
            case _, _, _:
                raise ValueError("Invalid segment.")

    def is_increasing(self, coordinate: str):
        match coordinate:
            case 'x':
                return self.start.x <= self.end.x
            case 'y':
                return self.start.y <= self.end.y


def read_segments(file_path: Path) -> List[Segment]:
    segments = []
    with open(file_path, 'r') as input_file:
        for line in input_file.read().split('\n'):
            start_point, end_point = line.split(' -> ')
            start_x, start_y = start_point.split(',')
            end_x, end_y = end_point.split(',')
            segments.append(
                Segment(
                    Point(int(start_x), int(start_y)),
                    Point(int(end_x), int(end_y))
                )
            )
    return segments


if __name__ == '__main__':
    input_file_path = INPUTS_FOLDER / Path(__file__).with_suffix('').name / 'input.txt'
    all_segments: List[Segment] = read_segments(file_path=input_file_path)

    # Part 1
    part_1_result: int = count_segment_overlaps(all_segments, use_diagonals=False)
    assert part_1_result == 5774
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_segment_overlaps(all_segments, use_diagonals=True)
    assert part_2_result == 18423
    print('Part 2 result :', part_2_result)
