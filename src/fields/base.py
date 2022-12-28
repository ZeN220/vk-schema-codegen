from typing import Optional, Union

from msgspec import Struct

from src.strings import is_valid_name, validate_field


class BaseField(Struct):
    type: Union[str, list]
    name: str
    required: bool = False
    """If required is not defined, it is assumed to be false."""
    description: Optional[str] = None

    @property
    def __typehint__(self) -> str:
        raise NotImplementedError

    def _get_required_field_class(self) -> str:
        if not self.required:
            raise ValueError("Field is not required")
        name_is_valid = is_valid_name(self.name)
        if not name_is_valid:
            name = validate_field(self.name)
            return (
                f"    {name}: {self.__typehint__} = pydantic.Field(\n"
                f'        alias="{self.name}"\n'
                f"    )\n"
            )
        return f"    {self.name}: {self.__typehint__}\n"

    def _get_optional_field_class(self) -> str:
        if self.required:
            raise ValueError("Field is required")
        name_is_valid = is_valid_name(self.name)
        if not name_is_valid:
            name = validate_field(self.name)
            return (
                f"    {name}: typing.Optional[{self.__typehint__}] = pydantic.Field(\n"
                f'        default=None, alias="{self.name}"\n'
                f"    )\n"
            )
        return f"    {self.name}: typing.Optional[{self.__typehint__}] = None\n"

    def _get_description(self) -> str:
        if self.description is None:
            return ""
        return f'    """{self.description}"""\n'

    def to_field_class(self):
        if self.required:
            string = self._get_required_field_class()
        else:
            string = self._get_optional_field_class()

        string += self._get_description()
        return string
