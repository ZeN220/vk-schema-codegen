from __future__ import annotations

from typing import Optional

from msgspec import Struct

from src.strings import to_camel_case

from .properties import BaseObjectProperty, get_property_from_dict


class BaseSchema(Struct):
    name: str


class ObjectSchema(BaseSchema):
    properties: list[BaseObjectProperty]

    @classmethod
    def from_dict(cls, name, properties: dict[str, dict]) -> ObjectSchema:
        result = []
        for property_name, property_value in properties.items():
            obj = get_property_from_dict(property_value, name=property_name)
            result.append(obj)
        schema = cls(name=name, properties=result)
        return schema

    def __str__(self):
        name = to_camel_case(self.name)
        class_string = f"class {name}(pydantic.BaseModel):\n"
        for property_ in self.properties:
            class_string += str(property_)
        class_string += "\n"
        return class_string


class EnumSchema(BaseSchema):
    type: str
    description: Optional[str] = None


class EnumStringSchema(EnumSchema):
    enum: list[str]
    enumNames: Optional[list[str]] = None
    """In schema of API this name is in CamelCase"""

    def __str__(self):
        name = to_camel_case(self.name)
        class_string = f"class {name}(enum.Enum):\n"
        if self.enumNames is not None:
            for enum, enum_name in zip(self.enum, self.enumNames):
                enum_name = enum_name.upper().replace(" ", "_")
                class_string += f'\t{enum_name} = "{enum}"\n'
        else:
            for enum in self.enum:
                enum_name = enum.upper()
                class_string += f'\t{enum_name} = "{enum_name}"\n'
        class_string += "\n"
        return class_string


class EnumIntegerSchema(EnumSchema):
    enum: list[int]
    enumNames: list[str]
    """In schema of API this name is in CamelCase"""
    default: Optional[int] = None
    minimum: Optional[int] = None

    def __str__(self):
        name = to_camel_case(self.name)
        class_string = f"class {name}(enum.IntEnum):\n"
        for enum, enum_name in zip(self.enum, self.enumNames):
            enum_name = enum_name.upper().replace(" ", "_")
            class_string += f"\t{enum_name} = {enum}\n"
        return class_string


def get_enum_from_dict(name: str, enum_data: dict) -> EnumSchema:
    if enum_data["type"] == "string":
        return EnumStringSchema(name=name, **enum_data)
    elif enum_data["type"] == "integer":
        return EnumIntegerSchema(name=name, **enum_data)
    raise ValueError(f"Unknown enum type: {enum_data}")
