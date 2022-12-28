from __future__ import annotations

from .base import BaseField


class OneOfField(BaseField):
    type: str = "oneOf"
    """
    This field is missing from original schema for this property,
    but it is required for parsing.
    """
    oneOf: list[BaseField]

    @property
    def __typehint__(self) -> str:
        typehints = [field.__typehint__ for field in self.oneOf]
        types = ", ".join(typehints)
        return f"typing.Union[{types}]"
