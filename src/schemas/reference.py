from __future__ import annotations

from src.strings import get_reference

from .base import BaseSchema


class ReferenceSchema(BaseSchema):
    reference: str

    @classmethod
    def from_dict(cls, name: str, data: dict) -> ReferenceSchema:
        schema = cls(name=name, reference=data["$ref"])
        return schema

    def to_class(self) -> str:
        reference = get_reference(self.reference)
        # fmt: off
        class_string = (
            f"class {self.name}({reference}):\n"
            f"    pass\n\n"
        )
        # fmt: on
        return class_string
