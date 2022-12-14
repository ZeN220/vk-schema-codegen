from .base import BaseProperty


class ArrayProperty(BaseProperty):
    type: str
    items: BaseProperty

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"

    def _get_description(self) -> dict:
        description_object = super()._get_description()
        if self.items.description is not None:
            description_object["Description of item of array"] = self.items.description
        return description_object
