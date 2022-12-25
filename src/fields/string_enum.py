from __future__ import annotations

from typing import Optional

from .string import StringField


class StringEnumField(StringField):
    __typehint__: str

    type: str
    enum: list[str]
    enumNames: Optional[list[str]] = None
