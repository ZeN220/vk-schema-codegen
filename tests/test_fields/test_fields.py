import pytest

from src.fields import (
    ArrayField,
    BaseField,
    BooleanField,
    DictField,
    FloatField,
    IntegerEnumField,
    IntegerField,
    OneOfField,
    PatternField,
    ReferenceField,
    StringEnumField,
    StringField,
    UnionField,
    get_enum_field_from_dict,
    get_field_from_dict,
)

MINIMUM_DATA: dict = {"name": "test_name"}


@pytest.mark.parametrize(
    "arguments, expected",
    [
        (
            {**MINIMUM_DATA, "item": {"type": "string"}},
            StringField(name="test_name", type="string"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "integer"}},
            IntegerField(name="test_name", type="integer"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "number"}},
            FloatField(name="test_name", type="number"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "boolean"}},
            BooleanField(name="test_name", type="boolean"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "object"}},
            DictField(name="test_name", type="object"),
        ),
        (
            {**MINIMUM_DATA, "item": {"$ref": "../dir/objects.json#/definitions/object"}},
            ReferenceField(name="test_name", reference="Object"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "array", "items": {"type": "object"}}},
            ArrayField(
                name="test_name", type="array", items=DictField(name="test_name", type="object")
            ),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": ["string", "integer"]}},
            UnionField(name="test_name", type=["string", "integer"]),
        ),
        (
            {**MINIMUM_DATA, "item": {"oneOf": [{"type": "string"}, {"type": "integer"}]}},
            OneOfField(
                name="test_name",
                oneOf=[
                    StringField(name="test_name", type="string"),
                    IntegerField(name="test_name", type="integer"),
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
            PatternField(
                type="object",
                name="test_name",
                patternProperties={"this_is_regexp": StringField(name="test_name", type="string")},
                additionalProperties=False,
            ),
        ),
    ],
)
def test_get_field_from_dict(arguments: dict, expected: BaseField):
    assert get_field_from_dict(**arguments) == expected


def test_get_field_from_dict_unknown():
    with pytest.raises(ValueError):
        get_field_from_dict(item={"type": "unknown"}, **MINIMUM_DATA)


@pytest.mark.parametrize(
    "arguments, expected",
    [
        (
            {
                **MINIMUM_DATA,
                "item": {"type": "string", "enum": ["a", "b", "c"]},
                "typehint": "TestTypeHint",
            },
            StringEnumField(
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
            IntegerEnumField(
                __typehint__="TestTypeHint",
                name="test_name",
                type="integer",
                enum=[1, 2, 3],
                enumNames=["a", "b", "c"],
            ),
        ),
    ],
)
def test_get_enum_field_from_dict(arguments: dict, expected: BaseField):
    assert get_enum_field_from_dict(**arguments) == expected


def test_get_enum_field_from_dict_unknown():
    with pytest.raises(ValueError):
        get_enum_field_from_dict(
            item={"type": "unknown"}, name="test_name", typehint="TestTypeHint"
        )
