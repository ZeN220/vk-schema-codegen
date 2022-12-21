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
    ReferenceField,
    StringArrayItem,
    StringEnumField,
    StringField,
    UnionField,
    get_property_from_dict,
)

MINIMUM_DATA: dict = {"object_name": "TestObject", "property_name": "test_name"}


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
            ReferenceField(name="test_name", reference="../dir/objects.json#/definitions/object"),
        ),
        (
            {**MINIMUM_DATA, "item": {"type": "array", "items": {"type": "string"}}},
            ArrayField(name="test_name", type="array", items=StringArrayItem(type="string")),
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
            {**MINIMUM_DATA, "item": {"type": "string", "enum": ["a", "b", "c"]}},
            StringEnumField(
                __typehint__="TestObjectTestName",
                name="test_name",
                type="string",
                enum=["a", "b", "c"],
            ),
        ),
        (
            {
                **MINIMUM_DATA,
                "item": {"type": "integer", "enum": [1, 2, 3], "enumNames": ["a", "b", "c"]},
            },
            IntegerEnumField(
                __typehint__="TestObjectTestName",
                name="test_name",
                type="integer",
                enum=[1, 2, 3],
                enumNames=["a", "b", "c"],
            ),
        ),
    ],
)
def test_get_property_from_dict(arguments: dict, expected: BaseField):
    assert get_property_from_dict(**arguments) == expected


def test_get_property_from_dict_raises():
    with pytest.raises(ValueError):
        get_property_from_dict(**MINIMUM_DATA, item={"type": "invalid"})
