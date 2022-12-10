from __future__ import annotations

from src.parsers.objects.array import BaseArrayItem, get_item_from_dict
from src.strings import to_camel_case

from .base import BaseSchema


class ArraySchema(BaseSchema):
    items: BaseArrayItem

    @classmethod
    def from_dict(cls, name, items: dict) -> ArraySchema:
        item = get_item_from_dict(items)
        schema = cls(name=name, items=item)
        return schema

    def __str__(self):
        name = to_camel_case(self.name)
        return f"{name} = list[{self.items.__typehint__}]\n\n"
