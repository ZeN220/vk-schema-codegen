from typing import Optional

from src.strings import is_valid_name, validate_field

from .base import BaseField


class ReferenceField(BaseField):
    type: str = "reference"
    """
    This field is missing from original schema for this property,
    but it is required for parsing.
    """
    reference: str
    default: Optional[str] = None

    @property
    def __typehint__(self) -> str:
        return self.reference

    def _get_default_field_class(self) -> str:
        if self.default is None:
            raise ValueError("Default value is not defined")
        name_is_valid = is_valid_name(self.name)
        # If reference to have default value, then this value is the field of enum
        default_value = f"{self.__typehint__}.{self.default.upper()}"
        if not name_is_valid:
            name = validate_field(self.name)
            return (
                f"    {name}: {self.__typehint__} = pydantic.Field(\n"
                f'        default={default_value}, alias="{self.name}"\n'
                f"    )\n"
            )
        return f"    {self.name}: {self.__typehint__} = {default_value}\n"

    def to_field_class(self):
        if self.default is not None:
            string = self._get_default_field_class()
        elif self.required:
            string = self._get_required_field_class()
        else:
            string = self._get_optional_field_class()

        string += self._get_description_field_class()
        return string
