from __future__ import annotations

from typing import Optional

from .string import StringProperty


class StringEnumProperty(StringProperty):
    __typehint__: str

    enum: list[str]
    enumNames: Optional[list[str]] = None
