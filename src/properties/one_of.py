from __future__ import annotations

from .base import BaseProperty


class OneOfProperty(BaseProperty):
    type: str = "oneOf"
    """
    This field is missing from original schema for this property,
    but it is required for parsing.
    """
    oneOf: list[BaseProperty]

    @property
    def __typehint__(self) -> str:
        typehints = [property_.__typehint__ for property_ in self.oneOf]
        types = ", ".join(typehints)
        return f"typing.Union[{types}]"
