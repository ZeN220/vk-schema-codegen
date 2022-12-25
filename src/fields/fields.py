from __future__ import annotations

from typing import Literal, Optional, Union

from msgspec import Struct

from src.strings import get_reference, is_valid_name, to_python_types, validate_field


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

    def to_field_class(self):
        if self.required:
            string = self._get_required_field_class()
        else:
            string = self._get_optional_field_class()

        if self.description is not None:
            string += f'    """{self.description}"""\n'
        return string


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

        if self.description is not None:
            string += f'    """{self.description}"""\n'
        return string


class StringField(BaseField):
    type: str
    maxLength: Optional[int] = None
    format: Optional[Literal["uri"]] = None

    @property
    def __typehint__(self) -> str:
        return "str"


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

        if self.description is not None:
            string += f'    """{self.description}"""\n'
        return string


class FloatField(BaseField):
    type: str
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[int] = None

    @property
    def __typehint__(self) -> str:
        return "float"


class BooleanField(BaseField):
    type: str
    default: Optional[bool] = None

    @property
    def __typehint__(self) -> str:
        return "bool"

    def _get_default_field_class(self) -> str:
        if self.default is None:
            raise ValueError("Default value is not defined")
        name_is_valid = is_valid_name(self.name)
        typehint = self.__typehint__
        if not name_is_valid:
            name = validate_field(self.name)
            return (
                f"    {name}: {typehint} = pydantic.Field(\n"
                f'        default={self.default}, alias="{self.name}"\n'
                f"    )\n"
            )
        return f"    {self.name}: {typehint} = {self.default}\n"

    def to_field_class(self):
        if self.default is not None:
            string = self._get_default_field_class()
        elif self.required:
            string = self._get_required_field_class()
        else:
            string = self._get_optional_field_class()

        if self.description is not None:
            string += f'    """{self.description}"""\n'
        return string


class DictField(BaseField):
    type: str

    @property
    def __typehint__(self) -> str:
        return "dict"


class ArrayField(BaseField):
    type: str
    items: BaseField

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"


class UnionField(BaseField):
    type: list[str]

    @property
    def __typehint__(self) -> str:
        python_types = to_python_types(self.type)
        types = ", ".join(python_types)
        return f"typing.Union[{types}]"


class OneOfField(BaseField):
    type: str = "oneOf"
    """
    This field is missing from original schema for this property,
    but it is required for parsing.
    """
    oneOf: list[BaseField]

    @property
    def __typehint__(self) -> str:
        typehints = [field.__typehint__ for field in self.oneOf]
        types = ", ".join(typehints)
        return f"typing.Union[{types}]"


class StringEnumField(StringField):
    __typehint__: str

    type: str
    enum: list[str]
    enumNames: Optional[list[str]] = None


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


class PatternField(BaseField):
    type: str = "patternProperties"
    """
    This field is missing from original schema for this property,
    but it is required for parsing.
    """
    patternProperties: dict[str, BaseField]
    additionalProperties: bool

    @property
    def __typehint__(self) -> str:
        typehints = [field.__typehint__ for field in self.patternProperties.values()]
        types = ", ".join(typehints)
        if len(typehints) == 1:
            return f"dict[str, {types}]"
        return f"dict[str, typing.Union[{types}]]"

    def to_field_class(self):
        if self.required:
            string = self._get_required_field_class()
        else:
            string = self._get_optional_field_class()

        if self.description is not None:
            string += f'    """\n' f"    {self.description}\n"
        else:
            string += '    """\n'

        string += "    Patterns of dict (as regexp) in the form of key-value:\n"
        for pattern, field in self.patternProperties.items():
            string += f"    {pattern}: {field.__typehint__}\n"
        string += '    """\n'
        return string


def get_field_from_dict(item: dict, name: str) -> BaseField:
    if item.get("$ref") is not None:
        copy_item = item.copy()
        ref = copy_item.pop("$ref")
        reference = get_reference(ref)
        return ReferenceField(name=name, reference=reference, **copy_item)
    if item.get("oneOf") is not None:
        copy_item = item.copy()
        one_of = copy_item.pop("oneOf")
        # Fields of oneOf are not required a name, but the function requires it.
        # So we add name of oneOf field
        one_of = [get_field_from_dict(item, name) for item in one_of]
        return OneOfField(name=name, oneOf=one_of, **copy_item)
    if item.get("patternProperties") is not None:
        copy_item = item.copy()
        pattern_properties = copy_item.pop("patternProperties")
        pattern_properties = {
            key: get_field_from_dict(value, name) for key, value in pattern_properties.items()
        }
        return PatternField(name=name, patternProperties=pattern_properties, **copy_item)

    field_type = item.get("type")
    if isinstance(field_type, list):
        return UnionField(name=name, **item)
    if field_type == "array":
        copy_item = item.copy()
        copy_item["items"] = get_field_from_dict(copy_item["items"], name)
        return ArrayField(name=name, **copy_item)
    if field_type == "object":
        return DictField(name=name, **item)
    if field_type == "integer":
        return IntegerField(name=name, **item)
    if field_type == "number":
        return FloatField(name=name, **item)
    if field_type == "boolean":
        return BooleanField(name=name, **item)
    if field_type == "string":
        # Some properties with the type "string" may have the field "minimum".
        # I do not know what it is for, so it is simply deleted
        copy_item = item.copy()
        copy_item.pop("minimum", None)
        return StringField(name=name, **copy_item)
    raise ValueError(f"Unknown field type: {field_type}")


def get_enum_field_from_dict(item: dict, name: str, typehint: str) -> BaseField:
    field_type = item["type"]
    if field_type == "string":
        return StringEnumField(name=name, __typehint__=typehint, **item)
    elif field_type == "integer":
        return IntegerEnumField(name=name, __typehint__=typehint, **item)
    raise ValueError(f"Unknown enum field type: {field_type}")
