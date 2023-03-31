import pytest

from src.properties import (
    ArrayProperty,
    BaseProperty,
    BooleanProperty,
    DictProperty,
    FloatProperty,
    IntegerEnumProperty,
    IntegerProperty,
    OneOfProperty,
    PatternProperty,
    ReferenceProperty,
    StringEnumProperty,
    StringProperty,
    UnionProperty,
    get_property,
)

MINIMUM_DATA: dict = {"name": "test_name", "typehint": "test_typehint"}


@pytest.mark.parametrize(
    "arguments, expected",
    [
        (
            {**MINIMUM_DATA, "item": {"type": "string"}},
            StringProperty(name="test_name", type="string"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "integer"}},
            IntegerProperty(name="test_name", type="integer"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "number"}},
            FloatProperty(name="test_name", type="number"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "boolean"}},
            BooleanProperty(name="test_name", type="boolean"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "object"}},
            DictProperty(name="test_name", type="object"),
        ),
        (
            {**MINIMUM_DATA, "item": {"$ref": "../dir/objects.json#/definitions/object"}},
            ReferenceProperty(name="test_name", reference="Object"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "array", "items": {"type": "object"}}},
            ArrayProperty(
                name="test_name", type="array", items=DictProperty(name="test_name", type="object")
            ),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": ["string", "integer"]}},
            UnionProperty(name="test_name", type=["string", "integer"]),
        ),
        (
            {**MINIMUM_DATA, "item": {"oneOf": [{"type": "string"}, {"type": "integer"}]}},
            OneOfProperty(
                name="test_name",
                oneOf=[
                    StringProperty(name="test_name", type="string"),
                    IntegerProperty(name="test_name", type="integer"),
                ],
            ),
        ),
        (
            {
                **MINIMUM_DATA,
                "item": {
                    "type": "object",
                    "patternProperties": {"this_is_regexp": {"type": "string"}},
                    "additionalProperties": False,
                },
            },
            PatternProperty(
                type="object",
                name="test_name",
                patternProperties={
                    "this_is_regexp": StringProperty(name="test_name", type="string")
                },
                additionalProperties=False,
            ),
        ),
        (
            {
                **MINIMUM_DATA,
                "item": {"type": "string", "enum": ["a", "b", "c"]},
                "typehint": "TestTypeHint",
            },
            StringEnumProperty(
                __typehint__="TestTypeHint",
                name="test_name",
                type="string",
                enum=["a", "b", "c"],
            ),
        ),
        (
            {
                **MINIMUM_DATA,
                "item": {"type": "integer", "enum": [1, 2, 3], "enumNames": ["a", "b", "c"]},
                "typehint": "TestTypeHint",
            },
            IntegerEnumProperty(
                __typehint__="TestTypeHint",
                name="test_name",
                type="integer",
                enum=[1, 2, 3],
                enumNames=["a", "b", "c"],
            ),
        ),
    ],
)
def test_get_property(arguments: dict, expected: BaseProperty):
    assert get_property(**arguments) == expected


@pytest.mark.parametrize("item", [{"type": "unknown"}, {"type": "unknown", "enum": ["a"]}])
def test_get_property_unknown(item):
    with pytest.raises(ValueError):
        get_property(item=item, **MINIMUM_DATA)
