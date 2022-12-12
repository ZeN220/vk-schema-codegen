from __future__ import annotations

from typing import Literal, Optional, Union

from msgspec import Struct

from src.strings import REFERENCE_REGEX, to_camel_case

from .array import BaseArrayItem, get_item_from_dict


class BaseField(Struct):
    type: Union[str, list]
    name: str
    required: bool = False
    """If required is not defined, it is assumed to be false."""
    description: Optional[str] = None

    @property
    def __typehint__(self) -> str:
        raise NotImplementedError

    def __str__(self):
        typehint = self.__typehint__
        if self.required:
            string = f"    {self.name}: {typehint}\n"
        else:
            string = f"    {self.name}: typing.Optional[{typehint}] = None\n"

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

    def get_reference(self) -> str:
        result = REFERENCE_REGEX.match(self.reference)
        if result is None:
            raise ValueError(f"Invalid reference: {self.reference}")
        return result.group(1)

    @property
    def __typehint__(self) -> str:
        reference = self.get_reference()
        return to_camel_case(reference)

    def __str__(self):
        typehint = self.__typehint__
        if self.default is not None:
            # If reference to have default value, then this value is the field of enum
            default_value = f"{typehint}.{self.default.upper()}"
            string = f"    {self.name}: {typehint} = {default_value}\n"
        elif self.required:
            string = f"    {self.name}: {typehint}\n"
        else:
            string = f"    {self.name}: typing.Optional[{typehint}] = None\n"

        if self.description is not None:
            string += f'    """{self.description}"""\n'
        return string


class StringField(BaseField):
    type: str
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

    def __str__(self):
        if self.default is not None:
            string = f"    {self.name}: int = {self.default}\n"
        elif self.required:
            string = f"    {self.name}: int\n"
        else:
            string = f"    {self.name}: typing.Optional[int] = None\n"

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

    def __str__(self):
        if self.default is not None:
            string = f"    {self.name}: bool = {self.default}\n"
        elif self.required:
            string = f"    {self.name}: bool\n"
        else:
            string = f"    {self.name}: typing.Optional[bool] = None\n"

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
    items: BaseArrayItem

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"


class UnionField(BaseField):
    type: list[str]

    @property
    def __typehint__(self) -> str:
        types = ", ".join(self.get_types())
        return f"typing.Union[{types}]"

    def get_types(self) -> list[str]:
        types = []
        for type_field in self.type:
            if type_field == "string":
                types.append("str")
            elif type_field == "integer":
                types.append("int")
            else:
                raise ValueError(f"Unknown union type: {type_field}")
        return types


class StringEnumProperty(StringField):
    type: str
    enum: list[str]
    enumNames: Optional[list[str]] = None

    @property
    def __typehint__(self) -> str:
        return to_camel_case(self.name)


class IntegerEnumProperty(IntegerField):
    type: str
    enum: list[int]
    enumNames: list[str]

    @property
    def __typehint__(self) -> str:
        return to_camel_case(self.name)


def get_property_from_dict(item: dict, name: str) -> BaseField:
    if name[0].isdigit():
        name = f"_{name}"

    if item.get("enum") is not None:
        return _get_enum_property(item, name)
    if item.get("$ref") is not None:
        reference = item.pop("$ref")
        return ReferenceField(name=name, reference=reference, **item)

    property_type = item.get("type")
    if isinstance(property_type, list):
        return UnionField(name=name, **item)
    if property_type == "array":
        item["items"] = get_item_from_dict(item["items"])
        return ArrayField(name=name, **item)
    if property_type == "object":
        return DictField(name=name, **item)
    if property_type == "string":
        # Some properties with the type "string" may have the field "minimum".
        # I do not know what it is for, so it is simply deleted
        item.pop("minimum", None)
        return StringField(name=name, **item)
    if property_type == "integer":
        return IntegerField(name=name, **item)
    if property_type == "number":
        return FloatField(name=name, **item)
    if property_type == "boolean":
        return BooleanField(name=name, **item)
    raise ValueError(f"Unknown property type: {property_type}")


def _get_enum_property(item: dict, name: str) -> BaseField:
    property_type = item["type"]
    if property_type == "string":
        return StringEnumProperty(name=name, **item)
    else:
        return IntegerEnumProperty(name=name, **item)
