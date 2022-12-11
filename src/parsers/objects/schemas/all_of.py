from __future__ import annotations

from msgspec import Struct

from src.strings import REFERENCE_REGEX, to_camel_case

from .base import BaseSchema
from .object import ObjectSchema


class AllOfObjectSchema(BaseSchema):
    object_schema: ObjectSchema
    """Last element from "allOf" object from schema"""
    allOf: list[ReferenceAllOf]

    @classmethod
    def from_dict(cls, name, all_of: list[dict]) -> AllOfObjectSchema:
        object_index = _get_index_object(all_of)
        object_schema = all_of.pop(object_index)
        object_schema = ObjectSchema.from_dict(name, object_schema["properties"])
        references = []
        for reference in all_of:
            reference = ReferenceAllOf(reference=reference["$ref"])
            references.append(reference)
        schema = cls(name=name, object_schema=object_schema, allOf=references)
        return schema

    def __str__(self):
        references = [reference.get_reference() for reference in self.allOf]
        child_classes = ", ".join(references)

        name = to_camel_case(self.name)
        class_string = f"class {name}({child_classes}):\n"
        for property_ in self.object_schema.properties:
            class_string += str(property_)
        class_string += "\n"
        return class_string


class ReferenceAllOf(Struct):
    reference: str

    def get_reference(self) -> str:
        reference = REFERENCE_REGEX.match(self.reference)
        if reference is None:
            raise ValueError(f"Invalid reference: {self.reference}")
        result = to_camel_case(reference.group(1))
        return result


def _get_index_object(all_of: list[dict]) -> int:
    for index, element in enumerate(all_of):
        if element.get("properties") is not None:
            return index
    raise ValueError("Invalid schema: no object found in 'allOf' list.")
