from typing import List, Tuple
from unittest import TestCase

from year_2020.solutions.python.utils.timing import decompose, parse_decomposed_duration, format_duration


class TestTiming(TestCase):

    def test_decompose_ns(self):
        # Given
        duration: int = 234

        # When
        decomposition: List[Tuple[int, str]] = decompose(duration)

        # Then
        expected_decomposition: List[Tuple[int, str]] = [(234, 'ns')]
        self.assertListEqual(expected_decomposition, decomposition)

    def test_decompose_us(self):
        # Given
        duration: int = 23456

        # When
        decomposition: List[Tuple[int, str]] = decompose(duration)

        # Then
        expected_decomposition: List[Tuple[int, str]] = [(23, 'μs'), (456, 'ns')]
        self.assertListEqual(expected_decomposition, decomposition)

    def test_decompose_ms(self):
        # Given
        duration: int = 1023456

        # When
        decomposition: List[Tuple[int, str]] = decompose(duration)

        # Then
        expected_decomposition: List[Tuple[int, str]] = [(1, 'ms'), (23, 'μs'), (456, 'ns')]
        self.assertListEqual(expected_decomposition, decomposition)

    def test_decompose_s(self):
        # Given
        duration: int = 45001023456

        # When
        decomposition: List[Tuple[int, str]] = decompose(duration)

        # Then
        expected_decomposition: List[Tuple[int, str]] = [(45, 's'), (1, 'ms'), (23, 'μs'), (456, 'ns')]
        self.assertListEqual(expected_decomposition, decomposition)

    def test_decompose_min(self):
        # Given
        duration: int = 65001023456

        # When
        decomposition: List[Tuple[int, str]] = decompose(duration)

        # Then
        expected_decomposition: List[Tuple[int, str]] = [(1, 'min'), (5, 's'), (1, 'ms'), (23, 'μs'), (456, 'ns')]
        self.assertListEqual(expected_decomposition, decomposition)

    def test_decompose_h(self):
        # Given
        duration: int = 7995125885088

        # When
        decomposition: List[Tuple[int, str]] = decompose(duration)

        # Then
        expected_decomposition: List[Tuple[int, str]] = [(2, 'h'), (13, 'min'), (15, 's'),
                                                         (125, 'ms'), (885, 'μs'), (88, 'ns')]
        self.assertListEqual(expected_decomposition, decomposition)

    def test_parse_decomposed_duration_ns(self):
        # Given
        decomposition: List[Tuple[int, str]] = [(234, 'ns')]

        # When
        parsed_duration: str = parse_decomposed_duration(decomposition)

        # Then
        expected_parsed_duration: str = '234 ns'
        self.assertEqual(expected_parsed_duration, parsed_duration)

    def test_parse_decomposed_duration_us(self):
        # Given
        decomposition: List[Tuple[int, str]] = [(23, 'μs'), (456, 'ns')]

        # When
        parsed_duration: str = parse_decomposed_duration(decomposition)

        # Then
        expected_parsed_duration: str = '23.456 μs'
        self.assertEqual(expected_parsed_duration, parsed_duration)

    def test_parse_decomposed_duration_ms(self):
        # Given
        decomposition: List[Tuple[int, str]] = [(1, 'ms'), (23, 'μs'), (456, 'ns')]

        # When
        parsed_duration: str = parse_decomposed_duration(decomposition)

        # Then
        expected_parsed_duration: str = '1.023 ms'
        self.assertEqual(expected_parsed_duration, parsed_duration)

    def test_parse_decomposed_duration_s(self):
        # Given
        decomposition: List[Tuple[int, str]] = [(45, 's'), (1, 'ms'), (23, 'μs'), (456, 'ns')]

        # When
        parsed_duration: str = parse_decomposed_duration(decomposition)

        # Then
        expected_parsed_duration: str = '45.001 s'
        self.assertEqual(expected_parsed_duration, parsed_duration)

    def test_parse_decomposed_duration_min(self):
        # Given
        decomposition: List[Tuple[int, str]] = [(1, 'min'), (5, 's'), (1, 'ms'), (23, 'μs'), (456, 'ns')]

        # When
        parsed_duration: str = parse_decomposed_duration(decomposition)

        # Then
        expected_parsed_duration: str = '1 min 5 s'
        self.assertEqual(expected_parsed_duration, parsed_duration)

    def test_parse_decomposed_duration_h(self):
        # Given
        decomposition: List[Tuple[int, str]] = [(2, 'h'), (13, 'min'), (15, 's'), (125, 'ms'), (885, 'μs'), (88, 'ns')]

        # When
        parsed_duration: str = parse_decomposed_duration(decomposition)

        # Then
        expected_parsed_duration: str = '2 h 13 min'
        self.assertEqual(expected_parsed_duration, parsed_duration)

    def test_format_duration_h(self):
        # Given
        duration_ns: int = 7995125885088

        # When
        formatted_duration: str = format_duration(duration_ns)

        # Then
        expected_formatted_duration: str = '2 h 13 min'
        self.assertEqual(expected_formatted_duration, formatted_duration)

    def test_format_duration_us(self):
        # Given
        duration_ns: int = 23456

        # When
        formatted_duration: str = format_duration(duration_ns)

        # Then
        expected_formatted_duration: str = '23.456 μs'
        self.assertEqual(expected_formatted_duration, formatted_duration)
