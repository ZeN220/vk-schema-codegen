from __future__ import annotations

from typing import Optional

from src.fields import BaseArrayItem, get_item_from_dict

from .base import BaseSchema


class ArraySchema(BaseSchema):
    type: str
    items: BaseArrayItem
    deprecated_from_version: Optional[str] = None
    minItems: Optional[int] = None
    maxItems: Optional[int] = None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, name, data: dict) -> ArraySchema:
        data["items"] = get_item_from_dict(data["items"])
        schema = cls(name=name, **data)
        return schema

    def to_class(self) -> str:
        string = f"{self.name} = list[{self.items.__typehint__}]"
        if self.description is not None:
            string += f"  # {self.description}"
        string += "\n\n"
        return string
