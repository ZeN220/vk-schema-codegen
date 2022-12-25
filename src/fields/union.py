from __future__ import annotations

from src.strings import to_python_types

from .base import BaseField


class UnionField(BaseField):
    type: list[str]

    @property
    def __typehint__(self) -> str:
        python_types = to_python_types(self.type)
        types = ", ".join(python_types)
        return f"typing.Union[{types}]"
