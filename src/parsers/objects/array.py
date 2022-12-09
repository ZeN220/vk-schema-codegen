from typing import Optional

from msgspec import Struct

from src.strings import REFERENCE_REGEX, to_camel_case


class BaseArrayItem(Struct):
    @property
    def __typehint__(self) -> str:
        raise NotImplementedError


class StringArrayItem(BaseArrayItem):
    __typehint__ = "str"

    type: str
    description: Optional[str] = None


class IntegerBaseArrayItem(BaseArrayItem):
    __typehint__ = "int"

    type: str
    description: Optional[str] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    default: Optional[int] = None


class ReferenceArrayItem(BaseArrayItem):
    reference: str
    """Alias for '$ref'"""

    @property
    def __typehint__(self) -> str:
        reference = REFERENCE_REGEX.match(self.reference)
        if reference is None:
            raise ValueError(f"Invalid reference: {self.reference}")
        result = to_camel_case(reference.group(1))
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
        return IntegerBaseArrayItem(**item)
    if item_type == "array":
        return NestedArrayItem(**item)
    raise ValueError(f"Unknown array item: {item_type}")
