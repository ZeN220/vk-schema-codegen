from typing import Literal, Optional

from msgspec import Struct

from src.strings import get_reference


class BaseArrayItem(Struct):
    @property
    def __typehint__(self) -> str:
        raise NotImplementedError


class StringArrayItem(BaseArrayItem):
    __typehint__ = "str"

    type: str
    description: Optional[str] = None


class IntegerArrayItem(BaseArrayItem):
    __typehint__ = "int"

    type: str
    description: Optional[str] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    default: Optional[int] = None
    entity: Optional[Literal["owner"]] = None
    format: Optional[Literal["int64"]] = None


class ReferenceArrayItem(BaseArrayItem):
    reference: str
    """Alias for '$ref'"""

    @property
    def __typehint__(self) -> str:
        result = get_reference(self.reference)
        return result


class NestedArrayItem(BaseArrayItem):
    type: str
    items: BaseArrayItem

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"


def get_item_from_dict(item: dict) -> BaseArrayItem:
    if item.get("$ref") is not None:
        return ReferenceArrayItem(reference=item["$ref"])

    item_type = item["type"]
    if item_type == "string":
        return StringArrayItem(**item)
    if item_type == "integer":
        return IntegerArrayItem(**item)
    if item_type == "array":
        return NestedArrayItem(**item)
    raise ValueError(f"Unknown array item: {item_type}")
