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


PROPERTIES_TYPES = {"$ref", "oneOf", "patternProperties", "type"}


def extract_property_type(item: dict) -> str:
    prop = list(filter(lambda x: x in PROPERTIES_TYPES, item.keys()))[0]
    return prop


class TypesHandler:
    def __init__(self, item_type):

        # dollar sign is not allowed in python variable name
        if item_type == "$ref":
            self.type = "ref"
        else:
            self.type = item_type

    def handle_item_type(self, item: dict, name: str) -> BaseProperty:
        method = getattr(self, f"build_from_{self.type}", self.build_from_unknown_type)
        return method(item, name)

    def build_from_ref(self, item: dict, name: str) -> BaseProperty:
        copy_item = item.copy()
        ref = copy_item.pop("$ref")
        reference = get_reference(ref)
        return ReferenceProperty(name=name, reference=reference, **copy_item)

    def build_from_oneOf(self, item: dict, name: str) -> BaseProperty:
        copy_item = item.copy()
        one_of_elements = copy_item.pop("oneOf")
        one_of = [get_property_from_dict(item, name) for item in one_of_elements]
        return OneOfProperty(name=name, oneOf=one_of, **copy_item)

    def build_from_patternProperties(self, item: dict, name: str) -> BaseProperty:
        copy_item = item.copy()
        pattern_properties = copy_item.pop("patternProperties")
        pattern_properties = {
            key: get_property_from_dict(value, name) for key, value in pattern_properties.items()
        }
        return PatternProperty(name=name, patternProperties=pattern_properties, **copy_item)

    def build_from_array(self, item: dict, name: str) -> BaseProperty:
        copy_item = item.copy()
        array_items = copy_item.pop("items")
        items = get_property_from_dict(array_items, name)
        return ArrayProperty(name=name, items=items, **copy_item)

    def build_from_object(self, item: dict, name: str) -> BaseProperty:
        return DictProperty(name=name, **item)

    def build_from_integer(self, item: dict, name: str) -> BaseProperty:
        return IntegerProperty(name=name, **item)

    def build_from_number(self, item: dict, name: str) -> BaseProperty:
        return FloatProperty(name=name, **item)

    def build_from_boolean(self, item: dict, name: str) -> BaseProperty:
        return BooleanProperty(name=name, **item)

    def build_from_string(self, item: dict, name: str) -> BaseProperty:
        # Some properties with the type "string" may have the field "minimum".
        # I do not know what it is for, so it is simply deleted
        copy_item = item.copy()
        copy_item.pop("minimum", None)
        return StringProperty(name=name, **copy_item)

    def build_from_unknown_type(self, item: dict, name: str) -> BaseProperty:
        raise ValueError(f"Unknown property type: {self.type}")

    def build_from_type(self, item: dict, name: str) -> BaseProperty:
        property_type = item.get("type")
        types_handler = TypesHandler(property_type)
        return types_handler.handle_item_type(item, name)


def get_property_from_dict(item: dict, name: str) -> BaseProperty:
    """
    Some properties have a nested properties, which are not defined names.
    So, this nested properties have a name of parent property.
    :param item: property as dict
    :param name: name of property
    :return: property as BaseProperty class
    """
    property_type = extract_property_type(item)
    types_handler = TypesHandler(property_type)

    return types_handler.handle_item_type(item, name)


def get_enum_property_from_dict(item: dict, name: str, typehint: str) -> BaseProperty:
    property_type = item["type"]
    if property_type == "string":
        return StringEnumProperty(name=name, __typehint__=typehint, **item)
    elif property_type == "integer":
        return IntegerEnumProperty(name=name, __typehint__=typehint, **item)
    raise ValueError(f"Unknown enum property type: {property_type}")
