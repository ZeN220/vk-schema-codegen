from __future__ import annotations

from typing import Literal, Optional, Union

from msgspec import Struct

from src.strings import REFERENCE_REGEX, to_camel_case

from .array import BaseArrayItem, get_item_from_dict


class BaseObjectProperty(Struct):
    type: str
    name: str
    required: bool = False
    """If required is not defined, it is assumed to be false."""
    description: Optional[str] = None

    @property
    def __typehint__(self) -> str:
        raise NotImplementedError

    def __str__(self):
        if self.name is None:
            raise TypeError("Element of list cannot have a string representation")
        typehint = self.__typehint__
        if self.required:
            string = f"    {self.name}: {typehint}\n"
        else:
            string = f"    {self.name}: typing.Optional[{typehint}] = None\n"

        if self.description is not None:
            string += f'    """{self.description}"""\n'
        return string


class ReferenceObjectProperty(BaseObjectProperty):
    type: str = "reference"
    """
    This field is missing from original schema for this property,
    but it is required for parsing.
    """
    reference: str

    def get_reference(self) -> str:
        result = REFERENCE_REGEX.match(self.reference)
        if result is None:
            raise ValueError(f"Invalid reference: {self.reference}")
        return result.group(1)

    @property
    def __typehint__(self) -> str:
        reference = self.get_reference()
        return to_camel_case(reference)


class StringObjectProperty(BaseObjectProperty):
    format: Optional[Literal["uri"]] = None

    @property
    def __typehint__(self) -> str:
        return "str"


class IntegerObjectProperty(BaseObjectProperty):
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


class FloatObjectProperty(BaseObjectProperty):
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[int] = None

    @property
    def __typehint__(self) -> str:
        return "float"


class BooleanObjectProperty(BaseObjectProperty):
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


class DictObjectProperty(BaseObjectProperty):
    @property
    def __typehint__(self) -> str:
        return "dict"


class ArrayObjectProperty(BaseObjectProperty):
    items: BaseArrayItem

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"


class StringEnumProperty(StringObjectProperty):
    enum: list[str]
    enumNames: Optional[list[str]] = None

    @property
    def __typehint__(self) -> str:
        return to_camel_case(self.name)


class IntegerEnumProperty(IntegerObjectProperty):
    enum: list[int]
    enumNames: list[str]

    @property
    def __typehint__(self) -> str:
        return to_camel_case(self.name)


def get_property_from_dict(item: dict, name: str) -> BaseObjectProperty:
    if name[0].isdigit():
        name = f"_{name}"

    if item.get("enum") is not None:
        return _get_enum_property(item, name)
    if item.get("$ref") is not None:
        reference = item.pop("$ref")
        return ReferenceObjectProperty(name=name, reference=reference, **item)

    property_type = item.get("type")
    if property_type == "array":
        item["items"] = get_item_from_dict(item["items"])
        return ArrayObjectProperty(name=name, **item)
    if property_type == "object":
        return DictObjectProperty(name=name, **item)
    if property_type == "string":
        return StringObjectProperty(name=name, **item)
    if property_type == "integer":
        return IntegerObjectProperty(name=name, **item)
    if property_type == "number":
        return FloatObjectProperty(name=name, **item)
    if property_type == "boolean":
        return BooleanObjectProperty(name=name, **item)
    raise ValueError(f"Unknown property type: {property_type}")


def _get_enum_property(item: dict, name: str) -> BaseObjectProperty:
    property_type = item["type"]
    if property_type == "string":
        return StringEnumProperty(name=name, **item)
    else:
        return IntegerEnumProperty(name=name, **item)
