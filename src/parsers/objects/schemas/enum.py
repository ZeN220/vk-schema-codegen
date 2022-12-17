from typing import Optional

from src.strings import to_camel_case, validate_field

from .base import BaseSchema


class EnumSchema(BaseSchema):
    type: str
    description: Optional[str] = None

    def to_class(self) -> str:
        raise NotImplementedError


class EnumStringSchema(EnumSchema):
    enum: list[str]
    enumNames: Optional[list[str]] = None

    def to_class(self) -> str:
        class_string = f"class {self.name}(enum.Enum):\n"
        if self.description is not None:
            class_string += f'    """{self.description}"""\n'

        if self.enumNames is not None:
            for enum, enum_name in zip(self.enum, self.enumNames):
                enum_name = enum_name.upper().replace(" ", "_")
                class_string += f'    {enum_name} = "{enum}"\n'
        else:
            for enum in self.enum:
                enum_name = enum.upper()
                class_string += f'    {enum_name} = "{enum}"\n'
        class_string += "\n"
        return class_string


class EnumIntegerSchema(EnumSchema):
    enum: list[int]
    enumNames: list[str]
    default: Optional[int] = None
    minimum: Optional[int] = None

    def to_class(self) -> str:
        class_string = f"class {self.name}(enum.IntEnum):\n"
        if self.description is not None:
            class_string += f'    """{self.description}"""\n'

        for enum, enum_name in zip(self.enum, self.enumNames):
            enum_name = enum_name.upper().replace(" ", "_")
            class_string += f"    {enum_name} = {enum}\n"
        class_string += "\n"
        return class_string


def get_enum_from_dict(name: str, enum_data: dict) -> EnumSchema:
    _validate_enum(enum_data)
    if enum_data["type"] == "string":
        return EnumStringSchema(name=name, **enum_data)
    elif enum_data["type"] == "integer":
        return EnumIntegerSchema(name=name, **enum_data)
    raise ValueError(f"Unknown enum type: {enum_data}")


def _validate_enum(enum_data: dict):
    names = []
    if enum_data.get("enumNames") is not None:
        enum_names = enum_data["enumNames"]
    else:
        enum_names = enum_data["enum"]

    for enum_name in enum_names:
        names.append(validate_field(enum_name))
    enum_data["enumNames"] = names


def get_enums_from_object(object_name: str, properties: dict[str, dict]) -> list[EnumSchema]:
    result = []
    properties = properties.copy()
    for property_name, data in properties.items():
        if data.get("enum") is None:
            continue
        # Property of enum can be required, but for generating enums class it is not needed
        data.pop("required", None)
        property_name = to_camel_case(f"{object_name}_{property_name}")
        enum = get_enum_from_dict(property_name, data)
        result.append(enum)
    return result


def get_enums_from_all_of(object_name: str, all_of: list[dict]) -> list[EnumSchema]:
    result = []
    for item in all_of:
        if item.get("properties") is not None:
            enums = get_enums_from_object(object_name, item["properties"])
            result.extend(enums)
    return result
