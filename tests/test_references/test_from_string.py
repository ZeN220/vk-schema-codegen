import pytest

from src.references.from_string import get_reference, parse_reference


@pytest.mark.parametrize(
    "reference, expected",
    [
        ("../directory/objects.json#/definitions/object", "object"),
        ("../anotherDirectory/objects.json#/definitions/object", "object"),
        ("../directory/objects.json#/definitions/another_object", "another_object"),
        ("../directory/objects.json#/definitions/anotherObject", "anotherObject"),
    ],
)
def test_parse_reference(reference: str, expected: str):
    assert parse_reference(reference) == expected


@pytest.mark.parametrize(
    "reference, expected",
    [
        ("../directory/objects.json#/definitions/object", "Object"),
        ("../directory/objects.json#/definitions/another_object", "AnotherObject"),
        ("../directory/objects.json#/definitions/anotherObject", "AnotherObject"),
    ],
)
def test_get_reference(reference: str, expected: str):
    assert get_reference(reference) == expected


def test_get_reference_unknown():
    reference = "../objects.json#/definitions/SomeObject"
    with pytest.raises(ValueError):
        get_reference(reference)
