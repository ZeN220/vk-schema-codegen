import pytest

from src.strings.validators import (
    is_valid_name,
    validate_field,
    validate_order_references,
)


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
def test_validate_field(string: str, expected: str):
    assert validate_field(string) == expected


@pytest.mark.parametrize(
    "objects, expected",
    [
        (
            {
                "A": {"allOf": [{"$ref": "../dir/objects.json#/definitions/B"}]},
                "B": {"allOf": [{"$ref": "../dir/objects.json#/definitions/C"}]},
                "C": {"type": "object"},
            },
            {
                "C": {"type": "object"},
                "B": {"allOf": [{"$ref": "../dir/objects.json#/definitions/C"}]},
                "A": {"allOf": [{"$ref": "../dir/objects.json#/definitions/B"}]},
            },
        ),
        (
            {
                "A": {"oneOf": [{"$ref": "../dir/objects.json#/definitions/B"}]},
                "B": {"type": "object"},
            },
            {
                "B": {"type": "object"},
                "A": {"oneOf": [{"$ref": "../dir/objects.json#/definitions/B"}]},
            },
        ),
        (
            {"A": {"$ref": "../dir/objects.json#/definitions/B"}, "B": {"type": "object"}},
            {"B": {"type": "object"}, "A": {"$ref": "../dir/objects.json#/definitions/B"}},
        ),
        (
            {"A": {"type": "object"}, "B": {"type": "object"}},
            {"A": {"type": "object"}, "B": {"type": "object"}},
        ),
    ],
)
def test_validate_order_references(objects: dict, expected: dict):
    assert validate_order_references(objects) == expected
