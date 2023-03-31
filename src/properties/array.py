from typing import Optional

from .base import BaseProperty


class ArrayProperty(BaseProperty):
    type: str
    items: BaseProperty

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"

    def _get_description(self) -> dict:
        description_object = super()._get_description()
        item_description = self._get_item_description()
        if item_description is not None:
            description_object["Description array item"] = item_description
        return description_object

    def _get_item_description(self) -> Optional[str]:
        item = self.items
        if item.description is not None:
            return item.description
        if isinstance(item, ArrayProperty):
            return item._get_item_description()
        return None
