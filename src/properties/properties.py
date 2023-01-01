from src.strings import get_reference

from .array import ArrayProperty
from .base import BaseProperty
from .boolean import BooleanProperty
from .dict import DictProperty
from .float import FloatProperty
from .integer import IntegerProperty
from .integer_enum import IntegerEnumProperty
from .one_of import OneOfProperty
from .pattern import PatternProperty
from .reference import ReferenceProperty
from .string import StringProperty
from .string_enum import StringEnumProperty
from .union import UnionProperty


def get_property_from_dict(item: dict, name: str) -> BaseProperty:
    """
    Some properties have a nested properties, which are not defined names.
    So, this nested properties have a name of parent property.
    :param item: property as dict
    :param name: name of property
    :return: property as BaseProperty class
    """
    if item.get("$ref") is not None:
        copy_item = item.copy()
        ref = copy_item.pop("$ref")
        reference = get_reference(ref)
        return ReferenceProperty(name=name, reference=reference, **copy_item)
    if item.get("oneOf") is not None:
        copy_item = item.copy()
        one_of_elements = copy_item.pop("oneOf")
        one_of = [get_property_from_dict(item, name) for item in one_of_elements]
        return OneOfProperty(name=name, oneOf=one_of, **copy_item)
    if item.get("patternProperties") is not None:
        copy_item = item.copy()
        pattern_properties = copy_item.pop("patternProperties")
        pattern_properties = {
            key: get_property_from_dict(value, name) for key, value in pattern_properties.items()
        }
        return PatternProperty(name=name, patternProperties=pattern_properties, **copy_item)

    property_type = item.get("type")
    if isinstance(property_type, list):
        return UnionProperty(name=name, **item)
    if property_type == "array":
        copy_item = item.copy()
        array_items = copy_item.pop("items")
        items = get_property_from_dict(array_items, name)
        return ArrayProperty(name=name, items=items, **copy_item)
    if property_type == "object":
        return DictProperty(name=name, **item)
    if property_type == "integer":
        return IntegerProperty(name=name, **item)
    if property_type == "number":
        return FloatProperty(name=name, **item)
    if property_type == "boolean":
        return BooleanProperty(name=name, **item)
    if property_type == "string":
        # Some properties with the type "string" may have the field "minimum".
        # I do not know what it is for, so it is simply deleted
        copy_item = item.copy()
        copy_item.pop("minimum", None)
        return StringProperty(name=name, **copy_item)
    raise ValueError(f"Unknown property type: {property_type}")


def get_enum_property_from_dict(item: dict, name: str, typehint: str) -> BaseProperty:
    property_type = item["type"]
    if property_type == "string":
        return StringEnumProperty(name=name, __typehint__=typehint, **item)
    elif property_type == "integer":
        return IntegerEnumProperty(name=name, __typehint__=typehint, **item)
    raise ValueError(f"Unknown enum property type: {property_type}")
