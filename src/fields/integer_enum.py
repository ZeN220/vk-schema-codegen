from __future__ import annotations

from src.strings import is_valid_name, validate_field

from .integer import IntegerField


class IntegerEnumField(IntegerField):
    __typehint__: str

    type: str
    enum: list[int]
    enumNames: list[str]

    def _get_default_enum(self) -> str:
        """
        Integer enum can have default value, for getting name of enum
        we need to get value of enum.
        :return: name of enum
        """
        for enum, enum_name in zip(self.enum, self.enumNames):
            if enum == self.default:
                return enum_name
        raise ValueError("Default value is not defined")

    def _get_default_field_class(self) -> str:
        if self.default is None:
            raise ValueError("Default value is not defined")
        name_is_valid = is_valid_name(self.name)
        default_value = self._get_default_enum()
        default = f"{self.__typehint__}.{default_value.upper()}"
        if not name_is_valid:
            name = validate_field(self.name)
            return (
                f"    {name}: {self.__typehint__} = pydantic.Field(\n"
                f'        default={default}, alias="{self.name}"\n'
                f"    )\n"
            )
        return f"    {self.name}: {self.__typehint__} = {default}\n"
