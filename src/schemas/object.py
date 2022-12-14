from __future__ import annotations

from src.properties import (
    BaseProperty,
    get_enum_property_from_dict,
    get_property_from_dict,
)
from src.strings import to_camel_case

from .base import BaseSchema


class ObjectSchema(BaseSchema):
    properties: list[BaseProperty]

    @classmethod
    def from_dict(cls, name, properties: dict[str, dict]) -> ObjectSchema:
        result = []
        for property_name, property_value in properties.items():
            if property_value.get("enum") is not None:
                typehint = to_camel_case(f"{name}_{property_name}")
                obj = get_enum_property_from_dict(
                    item=property_value, name=property_name, typehint=typehint
                )
            else:
                obj = get_property_from_dict(item=property_value, name=property_name)
            result.append(obj)
        schema = cls(name=name, properties=result)
        return schema

    def to_class(self) -> str:
        class_string = f"class {self.name}(pydantic.BaseModel):\n"
        for property_ in self.properties:
            class_string += property_.to_field_class()

        if not self.properties:
            class_string += "    pass\n"
        class_string += "\n"
        return class_string
