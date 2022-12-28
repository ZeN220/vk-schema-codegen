from __future__ import annotations

from typing import Optional

from msgspec import Struct

from src.strings import get_reference

from .base import BaseSchema
from .object import ObjectSchema


class AllOfSchema(BaseSchema):
    object_schema: Optional[ObjectSchema] = None
    """Last element from "allOf" object from schema"""
    allOf: list[ReferenceAllOf]

    @classmethod
    def from_dict(cls, name, all_of: list[dict]) -> AllOfSchema:
        # Because we need edit value of items, we need to copy it
        all_of = all_of.copy()
        try:
            object_index = _get_index_object(all_of)
        except ValueError:
            object_schema = None
        else:
            object_schema_dict = all_of.pop(object_index)
            object_schema = ObjectSchema.from_dict(name, object_schema_dict["properties"])

        references: list[ReferenceAllOf] = []
        for element in all_of:
            reference = ReferenceAllOf(reference=element["$ref"])
            references.append(reference)
        schema = cls(name=name, object_schema=object_schema, allOf=references)
        return schema

    def to_class(self) -> str:
        if self.name == "NewsfeedItemWallpost":
            # https://github.com/VKCOM/vk-api-schema/issues/203
            self.allOf.pop(0)
        references = [get_reference(element.reference) for element in self.allOf]
        child_classes = ", ".join(references)

        class_string = f"class {self.name}({child_classes}):\n"
        if len(class_string) > 100:
            child_classes = child_classes.replace(", ", ",\n    ")
            class_string = f"class {self.name}(\n    {child_classes}\n):\n"

        if self.object_schema is None:
            class_string += "    pass\n\n"
            return class_string

        for property_ in self.object_schema.properties:
            class_string += property_.to_field_class()
        class_string += "\n"
        return class_string


class ReferenceAllOf(Struct):
    reference: str


def _get_index_object(all_of: list[dict]) -> int:
    for index, element in enumerate(all_of):
        if element.get("properties") is not None:
            return index
    raise ValueError("Invalid schema: no object found in 'allOf' list.")
