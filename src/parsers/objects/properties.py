from __future__ import annotations

from typing import Literal, Optional, Type, Union

from msgspec import Struct

from src.strings import REFERENCE_REGEX, to_camel_case

from .array_items import ArrayItem, get_array_item_from_dict


class ObjectSchema(Struct):
    name: str
    properties: list[BaseObjectProperty]

    @classmethod
    def from_dict(cls, name, properties: dict[str, dict]) -> ObjectSchema:
        result = []
        for property_name, property_value in properties.items():
            obj = get_property_from_dict(property_value, name=property_name)
            result.append(obj)
        schema = cls(name=name, properties=result)
        return schema

    def __str__(self):
        name = to_camel_case(self.name)
        class_string = f"class {name}(pydantic.BaseModel):\n"
        for property_ in self.properties:
            class_string += str(property_)
        class_string += "\n"
        return class_string


class BaseObjectProperty(Struct):
    type: str
    name: str
    required: bool = False
    """If required is not defined, it is assumed to be false."""


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

    def __str__(self):
        reference = self.get_reference()
        annotation = to_camel_case(reference)
        if self.required:
            string = f"\t{self.name}: {annotation}\n"
        else:
            string = f"\t{self.name}: typing.Optional[{annotation}] = None\n"

        if self.description is not None:
            string += f'\t"""{self.description}"""\n'
        return string


class StringObjectProperty(BaseObjectProperty):
    description: Optional[str] = None
    format: Optional[Literal["uri"]] = None

    def __str__(self):
        if self.required:
            string = f"\t{self.name}: str\n"
        else:
            string = f"\t{self.name}: typing.Optional[str] = None\n"

        if self.description is not None:
            string += f'\t"""{self.description}"""\n'
        return string


class IntegerObjectProperty(BaseObjectProperty):
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
    description: Optional[str] = None
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[int] = None

    def __str__(self):
        if self.required:
            string = f"\t{self.name}: float\n"
        else:
            string = f"\t{self.name}: typing.Optional[float] = None\n"

        if self.description is not None:
            string += f'\t"""{self.description}"""\n'
        return string


class BooleanObjectProperty(BaseObjectProperty):
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
    def __str__(self):
        if self.required:
            return f"\t{self.name}: dict\n"
        return f"\t{self.name}: typing.Optional[dict] = None\n"


class ArrayObjectProperty(BaseObjectProperty):
    items: ArrayItem
    description: Optional[str] = None

    def __str__(self):
        annotation = self.items.__typehint__
        if self.required:
            string = f"\t{self.name}: list[{annotation}]\n"
        else:
            string = f"\t{self.name}: typing.Optional[list[{annotation}]] = None\n"

        if self.description is not None:
            string += f'\t"""{self.description}"""\n'
        return string


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


def get_property_from_dict(item: dict, name: str) -> BaseObjectProperty:
    if name[0].isdigit():
        name = f"_{name}"

    if item.get("enum") is not None:
        # TODO: Added class for property of enum
        pass
    if "$ref" in item:
        reference = item.pop("$ref")
        return ReferenceObjectProperty(name=name, reference=reference, **item)

    property_class = PROPERTIES.get(item["type"])
    if property_class is None:
        raise TypeError(f"Unknown property type: {item['type']}")
    if item["type"] == "array":
        item["items"] = get_array_item_from_dict(item["items"])
    return property_class(name=name, **item)
