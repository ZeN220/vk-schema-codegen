from typing import Optional

from msgspec import Struct

from src.strings import REFERENCE_REGEX


class ArrayItem(Struct):
    @property
    def __typehint__(self) -> str:
        raise NotImplementedError


class StringArrayItem(ArrayItem):
    __typehint__ = "str"

    type: str
    description: Optional[str] = None


class IntegerArrayItem(ArrayItem):
    __typehint__ = "int"

    type: str
    description: Optional[str] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    default: Optional[int] = None


class ReferenceArrayItem(ArrayItem):
    reference: str
    """This field it's a alias for '$ref'"""

    @property
    def __typehint__(self) -> str:
        result = REFERENCE_REGEX.match(self.reference)
        if result is None:
            raise ValueError(f"Invalid reference: {self.reference}")
        return result.group(1)


class NestedArrayItem(ArrayItem):
    type: str
    items: ArrayItem

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"


ARRAY_ITEMS = {
    "string": StringArrayItem,
    "integer": IntegerArrayItem,
    "array": NestedArrayItem,
}


def get_array_item_from_dict(data: dict) -> ArrayItem:
    if "$ref" in data:
        return ReferenceArrayItem(reference=data["$ref"])

    array_class = data.get(data["type"])
    if array_class is None:
        raise ValueError(f"Unknown array item: {data}")
    return array_class(**data)
