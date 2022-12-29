from typing import Literal, Optional

from .base import BaseField


class StringField(BaseField):
    type: str
    maxLength: Optional[int] = None
    format: Optional[Literal["uri"]] = None

    @property
    def __typehint__(self) -> str:
        return "str"

    def _get_description(self) -> dict:
        description_object = super()._get_description()
        if self.maxLength is not None:
            description_object["Max length"] = self.maxLength
        if self.format is not None:
            description_object["Format"] = self.format
        return description_object
