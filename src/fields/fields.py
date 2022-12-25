from src.strings import get_reference

from .array import ArrayField
from .base import BaseField
from .boolean import BooleanField
from .dict import DictField
from .float import FloatField
from .integer import IntegerField
from .integer_enum import IntegerEnumField
from .one_of import OneOfField
from .pattern import PatternField
from .reference import ReferenceField
from .string import StringField
from .string_enum import StringEnumField
from .union import UnionField


def get_field_from_dict(item: dict, name: str) -> BaseField:
    """
    Some fields have a nested fields, which are not defined names.
    So, this nested fields have a name of parent field.
    :param item: field as dict
    :param name: name of field
    :return: field as BaseField class
    """
    if item.get("$ref") is not None:
        copy_item = item.copy()
        ref = copy_item.pop("$ref")
        reference = get_reference(ref)
        return ReferenceField(name=name, reference=reference, **copy_item)
    if item.get("oneOf") is not None:
        copy_item = item.copy()
        one_of_elements = copy_item.pop("oneOf")
        one_of = [get_field_from_dict(item, name) for item in one_of_elements]
        return OneOfField(name=name, oneOf=one_of, **copy_item)
    if item.get("patternProperties") is not None:
        copy_item = item.copy()
        pattern_properties = copy_item.pop("patternProperties")
        pattern_properties = {
            key: get_field_from_dict(value, name) for key, value in pattern_properties.items()
        }
        return PatternField(name=name, patternProperties=pattern_properties, **copy_item)

    field_type = item.get("type")
    if isinstance(field_type, list):
        return UnionField(name=name, **item)
    if field_type == "array":
        copy_item = item.copy()
        array_items = copy_item.pop("items")
        items = get_field_from_dict(array_items, name)
        return ArrayField(name=name, items=items, **copy_item)
    if field_type == "object":
        return DictField(name=name, **item)
    if field_type == "integer":
        return IntegerField(name=name, **item)
    if field_type == "number":
        return FloatField(name=name, **item)
    if field_type == "boolean":
        return BooleanField(name=name, **item)
    if field_type == "string":
        # Some properties with the type "string" may have the field "minimum".
        # I do not know what it is for, so it is simply deleted
        copy_item = item.copy()
        copy_item.pop("minimum", None)
        return StringField(name=name, **copy_item)
    raise ValueError(f"Unknown field type: {field_type}")


def get_enum_field_from_dict(item: dict, name: str, typehint: str) -> BaseField:
    field_type = item["type"]
    if field_type == "string":
        return StringEnumField(name=name, __typehint__=typehint, **item)
    elif field_type == "integer":
        return IntegerEnumField(name=name, __typehint__=typehint, **item)
    raise ValueError(f"Unknown enum field type: {field_type}")
