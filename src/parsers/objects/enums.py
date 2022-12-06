from typing import Optional, Type

from msgspec import Struct

from src.strings import to_camel_case


class EnumSchema(Struct):
    type: str
    name: str
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


ENUMS: dict[str, Type[EnumSchema]] = {
    "string": EnumStringSchema,
    "integer": EnumIntegerSchema,
}


def get_enum_from_dict(name: str, enum_data: dict) -> EnumSchema:
    enum_class = ENUMS.get(enum_data["type"])
    if enum_class is None:
        raise ValueError(f"Unknown enum type: {enum_data}")
    return enum_class(name=name, **enum_data)
