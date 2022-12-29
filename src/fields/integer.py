from typing import Literal, Optional

from src.strings import is_valid_name, validate_field

from .base import BaseField


class IntegerField(BaseField):
    type: str
    default: Optional[int] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    entity: Optional[Literal["owner"]] = None
    format: Optional[Literal["int64"]] = None

    @property
    def __typehint__(self) -> str:
        return "int"

    def _get_description(self) -> dict:
        description_object = super()._get_description()
        if self.minimum is not None:
            description_object["Minimum value"] = self.minimum
        if self.maximum is not None:
            description_object["Maximum value"] = self.maximum
        if self.entity is not None:
            description_object["Entity"] = self.entity
        if self.format is not None:
            description_object["Format"] = self.format
        return description_object

    def _get_default_field_class(self) -> str:
        if self.default is None:
            raise ValueError("Default value is not defined")
        name_is_valid = is_valid_name(self.name)
        if not name_is_valid:
            name = validate_field(self.name)
            return (
                f"    {name}: {self.__typehint__} = pydantic.Field(\n"
                f'        default={self.default}, alias="{self.name}"\n'
                f"    )\n"
            )
        return f"    {self.name}: {self.__typehint__} = {self.default}\n"

    def to_field_class(self):
        if self.default is not None:
            string = self._get_default_field_class()
        elif self.required:
            string = self._get_required_field_class()
        else:
            string = self._get_optional_field_class()

        string += self._get_description_field_class()
        return string
