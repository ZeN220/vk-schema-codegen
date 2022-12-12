from __future__ import annotations

from typing import Optional

from src.fields import BaseArrayItem, get_item_from_dict
from src.strings import to_camel_case

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

    def __str__(self):
        name = to_camel_case(self.name)
        return f"{name} = list[{self.items.__typehint__}]  # {self.description}\n\n"
