from __future__ import annotations

from typing import Optional

from .base import BaseSchema


class BoolSchema(BaseSchema):
    type: str
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, name, data: dict) -> BoolSchema:
        schema = cls(name=name, **data)
        return schema

    def to_class(self) -> str:
        string = f"{self.name} = bool"
        if self.description is not None:
            string += f"  # {self.description}"
        string += "\n\n"
        return string
