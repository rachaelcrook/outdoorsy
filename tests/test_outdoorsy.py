import pytest

from cli import parse_args
from database import parse_delimiter, InvalidDelimiter

"""
def test():
    # Arrange
        set anything up
        build mock data
    
    # Act
        call the function you want to test
    
    # Assert
        check to make sure the results expected
"""


def test_parse_delimiter_comma():
    test_comma = parse_delimiter('comma')
    assert test_comma == ','


def test_parse_delimiter_pipe():
    test_comma = parse_delimiter('pipe')
    assert test_comma == '|'


def test_parse_delimiter_invalid():
    with pytest.raises(InvalidDelimiter):
        parse_delimiter('invalid')


def test_parse_args_with_file_and_delimiter():
    # Arrange
    mock_args = ['-f', '/path/to/my/dummy/file.csv', '-d', 'comma']

    # Act
    parsed_args = parse_args(mock_args)

    # Assert
    assert parsed_args.file == '/path/to/my/dummy/file.csv'
    assert parsed_args.delimiter == 'comma'


def test_parse_args_with_file_and_no_delimiter():
    # Arrange
    mock_args = ['-f', '/path/to/my/dummy/file.csv']

    # Act
    parsed_args = parse_args(mock_args)

    # Assert
    assert parsed_args.file == '/path/to/my/dummy/file.csv'


def test_parse_args_with_delimiter_and_no_file():
    # Arrange
    mock_args = ['-d', 'comma']

    # Act
    parsed_args = parse_args(mock_args)

    # Assert
    assert parsed_args.delimiter == 'comma'


def test_parse_args_with_view_and_sort_name():
    # Arrange
    mock_args = ['-v', '-s', 'name']

    # Act
    parsed_args = parse_args(mock_args)

    # Assert
    assert parsed_args.view
    assert parsed_args.sort == 'name'


def test_parse_args_with_view_and_sort_vehicle_type():
    # Arrange
    mock_args = ['-v', '-s', 'vehicle_type']

    # Act
    parsed_args = parse_args(mock_args)

    # Assert
    assert parsed_args.view
    assert parsed_args.sort == 'vehicle_type'


def test_parse_args_with_view_and_no_sort():
    # Arrange
    mock_args = ['-v']

    # Act
    parsed_args = parse_args(mock_args)

    # Assert
    assert parsed_args.view
