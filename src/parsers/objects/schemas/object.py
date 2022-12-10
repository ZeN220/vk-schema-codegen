from __future__ import annotations

from src.parsers.objects.properties import BaseObjectProperty, get_property_from_dict
from src.strings import to_camel_case

from .base import BaseSchema


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
