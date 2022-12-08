from __future__ import annotations

from typing import Literal, Optional, Type, Union

from msgspec import Struct

from src.strings import REFERENCE_REGEX, to_camel_case


class BaseObjectProperty(Struct):
    type: str
    name: Optional[str] = None
    """If property is a element of a list, this is the type of the list"""
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
            string = f"\t{self.name}: {typehint}\n"
        else:
            string = f"\t{self.name}: Optional[{typehint}] = None\n"

        if self.description is not None:
            string += f'\t"""{self.description}"""\n'
        return string


class ReferenceObjectProperty(BaseObjectProperty):
    type: str = "reference"
    """
    This field is missing from original schema for this property,
    but it is required for parsing.
    """
    reference: str
    description: Optional[str] = None

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
    __typehint__ = "str"

    description: Optional[str] = None
    format: Optional[Literal["uri"]] = None


class IntegerObjectProperty(BaseObjectProperty):
    __typehint__ = "int"

    description: Optional[str] = None
    default: Optional[int] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    entity: Optional[Literal["owner"]] = None
    format: Optional[Literal["int64"]] = None

    def __str__(self):
        if self.default is not None:
            string = f"\t{self.name}: int = {self.default}\n"
        elif self.required:
            string = f"\t{self.name}: int\n"
        else:
            string = f"\t{self.name}: typing.Optional[int] = None\n"

        if self.description is not None:
            string += f'\t"""{self.description}"""\n'
        return string


class FloatObjectProperty(BaseObjectProperty):
    __typehint__ = "float"

    description: Optional[str] = None
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[int] = None


class BooleanObjectProperty(BaseObjectProperty):
    __typehint__ = "bool"

    description: Optional[str] = None
    default: Optional[bool] = None

    def __str__(self):
        if self.default is not None:
            string = f"\t{self.name}: bool = {self.default}\n"
        elif self.required:
            string = f"\t{self.name}: bool\n"
        else:
            string = f"\t{self.name}: typing.Optional[bool] = None\n"

        if self.description is not None:
            string += f'\t"""{self.description}"""\n'
        return string


class DictObjectProperty(BaseObjectProperty):
    __typehint__ = "dict"


class ArrayObjectProperty(BaseObjectProperty):
    items: BaseObjectProperty
    description: Optional[str] = None

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"


# Because ReferenceObjectProperty doesn't have "type" field in schema of API,
# it's not available in this dict
PROPERTIES: dict[str, Type[BaseObjectProperty]] = {
    "string": StringObjectProperty,
    "integer": IntegerObjectProperty,
    "number": FloatObjectProperty,
    "boolean": BooleanObjectProperty,
    "object": DictObjectProperty,
    "array": ArrayObjectProperty,
}


def get_property_from_dict(
    item: dict, name: Optional[str] = None
) -> BaseObjectProperty:
    if name is not None and name[0].isdigit():
        name = f"_{name}"

    if item.get("enum") is not None:
        # TODO: Added class for property of enum
        pass
    if item.get("$ref") is not None:
        reference = item.pop("$ref")
        return ReferenceObjectProperty(name=name, reference=reference, **item)

    property_class = PROPERTIES.get(item["type"])
    if property_class is None:
        raise TypeError(f"Unknown property type: {item['type']}")
    if item["type"] == "array":
        item["items"] = get_property_from_dict(item["items"])
    return property_class(name=name, **item)
