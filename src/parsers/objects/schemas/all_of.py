from __future__ import annotations

from src.parsers.objects.properties import ReferenceObjectProperty
from src.strings import to_camel_case

from .base import BaseSchema
from .object import ObjectSchema


class AllOfObjectSchema(BaseSchema):
    object_schema: ObjectSchema
    """Last element from "allOf" object from schema"""
    allOf: list[ReferenceObjectProperty]

    @classmethod
    def from_dict(cls, name, all_of: list[dict]) -> AllOfObjectSchema:
        object_schema = all_of.pop(-1)
        object_schema = ObjectSchema.from_dict(name, object_schema["properties"])
        references = []
        for reference in all_of:
            reference = ReferenceObjectProperty(reference=reference["$ref"])
            references.append(reference)
        schema = cls(name=name, object_schema=object_schema, allOf=references)
        return schema

    def __str__(self):
        name = to_camel_case(self.name)
        child_classes = ", ".join([reference.__typehint__ for reference in self.allOf])
        class_string = f"class {name}({child_classes}):\n"
        for property_ in self.object_schema.properties:
            class_string += str(property_)
        class_string += "\n"
        return class_string
