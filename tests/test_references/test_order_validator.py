import pytest

from src.references import validate_order_references


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
