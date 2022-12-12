from typing import Optional

from src.strings import to_camel_case

from .base import BaseSchema


class EnumSchema(BaseSchema):
    type: str
    description: Optional[str] = None


class EnumStringSchema(EnumSchema):
    enum: list[str]
    enumNames: Optional[list[str]] = None

    def __str__(self):
        # fmt: off
        class_string = (
            f'class {self.name}(enum.Enum):\n'
            f'    """{self.description}"""\n'
        )
        # fmt: on
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

    def __str__(self):
        # fmt: off
        class_string = (
            f'class {self.name}(enum.IntEnum):\n'
            f'    """{self.description}"""\n'
        )
        # fmt: on
        for enum, enum_name in zip(self.enum, self.enumNames):
            enum_name = enum_name.upper().replace(" ", "_")
            class_string += f"    {enum_name} = {enum}\n"
        class_string += "\n"
        return class_string


def get_enum_from_dict(name: str, enum_data: dict) -> EnumSchema:
    if enum_data["type"] == "string":
        return EnumStringSchema(name=name, **enum_data)
    elif enum_data["type"] == "integer":
        return EnumIntegerSchema(name=name, **enum_data)
    raise ValueError(f"Unknown enum type: {enum_data}")


def get_enums_from_properties(object_name: str, properties: dict[str, dict]) -> list[EnumSchema]:
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
