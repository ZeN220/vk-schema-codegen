import pytest

from src.references import parse_objects_references


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
def test_parse_objects_reference(response, expected):
    test_response = {"response": {"properties": {"response": response}}}
    assert parse_objects_references(test_response) == expected
