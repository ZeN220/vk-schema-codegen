import pytest

from src.fields import (
    BaseArrayItem,
    IntegerArrayItem,
    NestedArrayItem,
    ReferenceArrayItem,
    StringArrayItem,
    UnionArrayItem,
    get_item_from_dict,
)


def test_array_item_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseArrayItem().__typehint__  # noqa


@pytest.mark.parametrize(
    "arguments, expected",
    [
        ({"type": "string"}, StringArrayItem(type="string")),
        ({"type": "integer"}, IntegerArrayItem(type="integer")),
        ({"type": ["string", "integer"]}, UnionArrayItem(type=["string", "integer"])),
        (
            {"$ref": "../dir/objects.json#/definitions/object"},
            ReferenceArrayItem(reference="Object"),
        ),
        (
            {"type": "array", "items": {"type": "string"}},
            NestedArrayItem(type="array", items=StringArrayItem(type="string")),
        ),
    ],
)
def test_get_item_from_dict(arguments: dict, expected: BaseArrayItem):
    assert get_item_from_dict(arguments) == expected


def test_get_item_from_dict_unknown_type():
    with pytest.raises(ValueError):
        get_item_from_dict({"type": "unknown"})
