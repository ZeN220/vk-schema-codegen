from typing import Optional, Union

from .base import BaseField


class FloatField(BaseField):
    type: str
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[int] = None

    @property
    def __typehint__(self) -> str:
        return "float"

    def _get_description(self) -> dict:
        description_object = super()._get_description()
        if self.minimum is not None:
            description_object["Minimum value"] = self.minimum
        if self.maximum is not None:
            description_object["Maximum value"] = self.maximum
        return description_object
