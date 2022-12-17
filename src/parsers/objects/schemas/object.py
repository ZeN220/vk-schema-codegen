from __future__ import annotations

from src.fields import BaseField, get_property_from_dict

from .base import BaseSchema


class ObjectSchema(BaseSchema):
    properties: list[BaseField]

    @classmethod
    def from_dict(cls, name, properties: dict[str, dict]) -> ObjectSchema:
        result = []
        for property_name, property_value in properties.items():
            obj = get_property_from_dict(object_name=name, name=property_name, item=property_value)
            result.append(obj)
        schema = cls(name=name, properties=result)
        return schema

    def to_class(self) -> str:
        class_string = f"class {self.name}(pydantic.BaseModel):\n"
        for property_ in self.properties:
            class_string += property_.to_field_class()

        if not self.properties:
            class_string += "   pass\n"
        class_string += "\n"
        return class_string
