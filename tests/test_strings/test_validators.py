import pytest

from src.strings.validators import is_valid_name, validate_name


@pytest.mark.parametrize(
    "string, expected",
    [
        ("test", True),
        ("123_name", False),
        ("global", False),
    ],
)
def test_is_valid_name(string: str, expected: bool):
    assert is_valid_name(string) == expected


@pytest.mark.parametrize(
    "string, expected",
    [
        ("string", "string"),
        ("1string", "_1string"),
        ("class", "class_"),
    ],
)
def test_validate_name(string: str, expected: str):
    assert validate_name(string) == expected
