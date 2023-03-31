from __future__ import annotations

import re
from typing import Literal, Optional

from src.properties import BaseProperty, get_property
from src.strings import to_camel_case

from .base import BaseSchema

METHOD_NAME_REGEXP = re.compile(r"(\w+)\.(\w+)")


class MethodSchema(BaseSchema):
    name: str
    access_token_type: list[Literal["open", "user", "group", "service", "anonymous"]]
    parameters: list[BaseProperty]
    responses: list[str]
    errors: Optional[list[str]] = None

    @classmethod
    def from_dict(cls, data: dict) -> MethodSchema:
        parse_data = parse_method_name(data["name"])
        name = parse_data["method"]
        section_name = parse_data["section"]
        access_token_type = data["access_token_type"]
        responses = parse_method_responses(data["responses"])

        parameters = []
        raw_parameters = data["parameters"].copy()
        for raw_parameter in raw_parameters:
            name_parameter = raw_parameter.pop("name")
            typehint = to_camel_case("_".join([section_name, name, name_parameter]))
            parameter = get_property(raw_parameter, name_parameter, typehint)
            parameters.append(parameter)

        return cls(
            name=name,
            access_token_type=access_token_type,
            parameters=parameters,
            responses=responses,
        )


def parse_method_name(string: str) -> dict[str, str]:
    result = METHOD_NAME_REGEXP.match(string)
    if result is None:
        raise ValueError(f"Can't parse method name {string}")
    return {
        "section": result.group(1),
        "method": result.group(2),
    }


def parse_method_responses(responses: dict[str, dict]) -> list[str]:
    result = []
    for response in responses.values():
        result.append(response["$ref"])
    return result
