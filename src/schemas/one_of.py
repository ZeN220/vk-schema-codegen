from __future__ import annotations

import copy
from typing import Optional

from msgspec import Struct

from src.strings import get_reference, to_python_type

from .base import BaseSchema


class OneOfSchema(BaseSchema):
    oneOf: list[ElementOneOf]

    @classmethod
    def from_dict(cls, name, one_of: list[dict]) -> OneOfSchema:
        one_of_elements: list[ElementOneOf] = []
        # Because we need edit value of items in nested schemas,
        # we need to call copy.deepcopy for copy
        one_of = copy.deepcopy(one_of)
        for element in one_of:
            if element.get("$ref") is not None:
                ref = element.pop("$ref")
                reference = ReferenceOneOf(reference=ref, **element)
                one_of_elements.append(reference)
            else:
                element_type = to_python_type(element.pop("type"))
                one_of_elements.append(ElementOneOf(type=element_type, **element))
        schema = cls(name=name, oneOf=one_of_elements)
        return schema

    def to_class(self) -> str:
        union_types = []
        for element in self.oneOf:
            if isinstance(element, ReferenceOneOf):
                typehint = get_reference(element.reference)
                union_types.append(typehint)
            else:
                union_types.append(element.type)
        types = ", ".join(union_types)
        string = f"{self.name} = typing.Union[{types}]\n\n"
        if len(string) > 100:
            types = types.replace(", ", ",\n    ")
            string = f"{self.name} = typing.Union[\n    {types}\n]\n\n"
        return string


class ElementOneOf(Struct):
    type: str


class ReferenceOneOf(ElementOneOf):
    type: str = "reference"
    reference: str
    description: Optional[str] = None
