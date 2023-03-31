from __future__ import annotations

from typing import Optional

from src.properties import BaseProperty, get_property

from .base import BaseSchema


class ArraySchema(BaseSchema):
    type: str
    items: BaseProperty
    deprecated_from_version: Optional[str] = None
    minItems: Optional[int] = None
    maxItems: Optional[int] = None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, name: str, data: dict) -> ArraySchema:
        # Because we need edit value of items, we need to copy it
        copy_data = data.copy()
        typehint = name + "Enum"
        copy_data["items"] = get_property(copy_data["items"], name, typehint)
        schema = cls(name=name, **copy_data)
        return schema

    def to_class(self) -> str:
        string = f"{self.name} = list[{self.items.__typehint__}]"
        if self.description is not None:
            string += f"  # {self.description}"
        string += "\n\n"
        return string
