from __future__ import annotations

from typing import Optional, Literal, Union
import re

from msgspec import Struct


class ObjectSchema(Struct):
    name: str
    properties: list["BaseObjectProperty"]

    def __str__(self):
        name = to_camel_case(self.name)
        class_string = f"class {name}(BaseModel):\n"
        for property_ in self.properties:
            class_string += str(property_)
        class_string += "\n"
        return class_string


class BaseObjectProperty(Struct):
    type: str
    name: Optional[str] = None
    """If property is a element of a list, it does not have a name"""
    required: bool = False
    """If required is not defined, it is assumed to be false."""


class ReferenceObjectProperty(BaseObjectProperty):
    REFERENCE_REGEX = re.compile(r"\.\./[a-z]+/objects\.json#/definitions/([a-z_]+)")
    
    type: str = "reference"
    """
    This field is missing from original schema for this property, 
    but it is required for parsing.
    """
    reference: str
    description: Optional[str] = None
    
    def get_reference(self) -> str:
        return self.REFERENCE_REGEX.match(self.reference).group(1)

    def __str__(self):
        reference = self.get_reference()
        annotation = to_camel_case(reference)
        if self.required:
            return f"\t{self.name}: {annotation}\n"
        return f"\t{self.name}: typing.Optional[{annotation}] = None\n"


class StringObjectProperty(BaseObjectProperty):
    description: str
    format: Optional[Literal["uri"]] = None

    def __str__(self):
        if self.required:
            return f"\t{self.name}: str\n"
        return f"\t{self.name}: typing.Optional[str] = None\n"


class IntegerObjectProperty(BaseObjectProperty):
    description: Optional[str] = None
    default: Optional[int] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    entity: Optional[Literal["owner"]] = None
    format: Optional[Literal["int64"]] = None

    def __str__(self):
        if self.default is not None:
            return f"\t{self.name}: int = {self.default}\n"
        if self.required:
            return f"\t{self.name}: int\n"
        return f"\t{self.name}: typing.Optional[int] = None\n"


class FloatObjectProperty(BaseObjectProperty):
    description: Optional[str] = None
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[int] = None

    def __str__(self):
        if self.required:
            return f"\t{self.name}: float\n"
        return f"\t{self.name}: typing.Optional[float] = None\n"


class BooleanObjectProperty(BaseObjectProperty):
    description: Optional[str] = None
    default: Optional[bool] = None

    def __str__(self):
        if self.default is not None:
            return f"\t{self.name}: bool = {self.default}\n"
        if self.required:
            return f"\t{self.name}: bool\n"
        return f"\t{self.name}: typing.Optional[bool] = None\n"


class DictObjectProperty(BaseObjectProperty):
    def __str__(self):
        if self.required:
            return f"\t{self.name}: dict\n"
        return f"\t{self.name}: typing.Optional[dict] = None\n"


class ArrayObjectProperty(BaseObjectProperty):
    items: BaseObjectProperty
    description: Optional[str] = None

    def __str__(self):
        annotation = self.get_annotation()
        if self.required:
            return f"\t{self.name}: list[{annotation}]\n"
        return f"\t{self.name}: typing.Optional[list[{annotation}]] = None\n"
    
    def get_annotation(self) -> str:
        if isinstance(self.items, ReferenceObjectProperty):
            reference = self.items.get_reference()
            return to_camel_case(reference)
        if isinstance(self.items, StringObjectProperty):
            return "str"
        if isinstance(self.items, IntegerObjectProperty):
            return "int"
        if isinstance(self.items, FloatObjectProperty):
            return "float"
        if isinstance(self.items, BooleanObjectProperty):
            return "bool"
        raise TypeError("Unsupported property type")


def to_camel_case(snake_str: str) -> str:
    result = snake_str.title().replace("_", "")
    return result
