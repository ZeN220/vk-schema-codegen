import pytest

from src.strings.reference import (
    get_reference,
    parse_reference,
    parse_responses_references,
)


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


@pytest.mark.parametrize(
    "response, expected",
    [
        (
            {"$ref": "../directory/objects.json#/definitions/object"},
            {"Object"},
        ),
        (
            {"type": "array", "items": {"type": "string"}},
            set(),
        ),
        (
            {
                "type": "array",
                "items": {"$ref": "../directory/objects.json#/definitions/object"},
            },
            {"Object"},
        ),
        (
            {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"$ref": "../directory/objects.json#/definitions/object"},
                    },
                },
            },
            {"Object"},
        ),
        (
            {
                "type": "object",
                "properties": {
                    "test_property": {
                        "type": "array",
                        "items": {"$ref": "../directory/objects.json#/definitions/object"},
                    },
                    "test_another_property": {
                        "$ref": "../directory/objects.json#/definitions/another_object"
                    },
                },
            },
            {"Object", "AnotherObject"},
        ),
        (
            {
                "type": "object",
                "patternProperties": {
                    "this_is_regexp": {"$ref": "../directory/objects.json#/definitions/object"}
                },
            },
            {"Object"},
        ),
    ],
)
def test_parse_responses_reference(response, expected):
    test_response = {"response": {"properties": {"response": response}}}
    assert parse_responses_references(test_response) == expected
