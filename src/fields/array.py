from typing import Literal, Optional

from msgspec import Struct

from src.strings import get_reference, to_python_types


class BaseArrayItem(Struct):
    @property
    def __typehint__(self) -> str:
        raise NotImplementedError


class StringArrayItem(BaseArrayItem):
    type: str
    description: Optional[str] = None

    @property
    def __typehint__(self) -> str:
        return "str"


class IntegerArrayItem(BaseArrayItem):
    type: str
    description: Optional[str] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    default: Optional[int] = None
    entity: Optional[Literal["owner"]] = None
    format: Optional[Literal["int64"]] = None

    @property
    def __typehint__(self) -> str:
        return "int"


class UnionArrayItem(BaseArrayItem):
    type: list[str]

    @property
    def __typehint__(self) -> str:
        types = ", ".join(to_python_types(self.type))
        return f"typing.Union[{types}]"


class ReferenceArrayItem(BaseArrayItem):
    reference: str
    """Alias for '$ref'"""

    @property
    def __typehint__(self) -> str:
        return self.reference


class NestedArrayItem(BaseArrayItem):
    type: str
    items: BaseArrayItem

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"


def get_item_from_dict(item: dict) -> BaseArrayItem:
    if item.get("$ref") is not None:
        reference = get_reference(item["$ref"])
        return ReferenceArrayItem(reference=reference)

    item_type = item["type"]
    if isinstance(item_type, list):
        return UnionArrayItem(**item)
    if item_type == "string":
        return StringArrayItem(**item)
    if item_type == "integer":
        return IntegerArrayItem(**item)
    if item_type == "array":
        copy_item = item.copy()
        copy_item["items"] = get_item_from_dict(copy_item["items"])
        return NestedArrayItem(**copy_item)
    raise ValueError(f"Unknown array item: {item_type}")
