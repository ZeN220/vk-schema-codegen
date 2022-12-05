from typing import Optional

from msgspec import Struct

from src.strings import to_camel_case


class ArrayItem(Struct):
    pass


class StringArrayItem(ArrayItem):
    type: str
    description: Optional[str] = None


class ReferenceArrayItem(ArrayItem):
    reference: str
    """This field it's a alias for '$ref'"""


class IntegerArrayItem(ArrayItem):
    type: str
    description: Optional[str] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    default: Optional[int] = None


class NestedArrayItem(ArrayItem):
    type: str
    items: ArrayItem

    def get_annotation(self) -> str:
        # Fucking copy past...
        if isinstance(self.items, StringArrayItem):
            return "str"
        if isinstance(self.items, IntegerArrayItem):
            return "int"
        if isinstance(self.items, ReferenceArrayItem):
            return to_camel_case(self.items.reference)
        # Missing here "NestedArrayItem" because API doesn't have 3-dimensional and more arrays
        raise TypeError("Unsupported property type")
