from __future__ import annotations

from typing import Optional

from src.fields import BaseField, get_field_from_dict

from .base import BaseSchema


class ArraySchema(BaseSchema):
    type: str
    items: BaseField
    deprecated_from_version: Optional[str] = None
    minItems: Optional[int] = None
    maxItems: Optional[int] = None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, name, data: dict) -> ArraySchema:
        # Because we need edit value of items, we need to copy it
        copy_data = data.copy()
        copy_data["items"] = get_field_from_dict(copy_data["items"], name)
        schema = cls(name=name, **copy_data)
        return schema

    def to_class(self) -> str:
        string = f"{self.name} = list[{self.items.__typehint__}]"
        if self.description is not None:
            string += f"  # {self.description}"
        string += "\n\n"
        return string
