from __future__ import annotations

from typing import Optional

from msgspec import Struct

from src.strings import get_reference, to_python_types

from .base import BaseSchema


class OneOfSchema(BaseSchema):
    oneOf: Optional[list[ReferenceOneOf]] = None
    types: Optional[list[str]] = None
    """Some objects, which have "oneOf" field, are not classes, but just union type."""

    @classmethod
    def from_dict(cls, name, one_of: list[dict]) -> OneOfSchema:
        references = []
        if any(element.get("$ref") is None for element in one_of):
            types = [element["type"] for element in one_of]
            python_types = to_python_types(types)
            return cls(name=name, types=python_types)
        for reference in one_of:
            ref = reference.pop("$ref")
            reference = ReferenceOneOf(reference=ref, **reference)
            references.append(reference)
        schema = cls(name=name, oneOf=references)
        return schema

    def __str__(self):
        if self.oneOf is not None:
            return self._get_one_of_string()
        types = ", ".join(self.types)
        return f"{self.name} = typing.Union[{types}]\n\n"

    def _get_one_of_string(self):
        references = [get_reference(element.reference) for element in self.oneOf]
        child_classes = ", ".join(references)

        class_string = f"class {self.name}({child_classes}):\n"
        class_string += "    pass\n\n"
        return class_string


class ReferenceOneOf(Struct):
    reference: str
    description: Optional[str] = None
