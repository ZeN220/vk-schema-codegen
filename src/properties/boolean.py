from typing import Optional, Union

from src.strings import is_valid_name, validate_name

from .base import BaseProperty


class BooleanProperty(BaseProperty):
    type: str
    default: Optional[Union[bool, int]] = None

    @property
    def __typehint__(self) -> str:
        return "bool"

    def _get_default_field_class(self) -> str:
        if self.default is None:
            raise ValueError("Default value is not defined")
        name_is_valid = is_valid_name(self.name)
        typehint = self.__typehint__
        default = bool(self.default)
        if not name_is_valid:
            name = validate_name(self.name)
            return (
                f"    {name}: {typehint} = pydantic.Field(\n"
                f'        default={default}, alias="{self.name}"\n'
                f"    )\n"
            )
        return f"    {self.name}: {typehint} = {default}\n"

    def to_field_class(self) -> str:
        if self.default is not None:
            string = self._get_default_field_class()
        elif self.required:
            string = self._get_required_field_class()
        else:
            string = self._get_optional_field_class()

        string += self._get_description_field_class()
        return string
