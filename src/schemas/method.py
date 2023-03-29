from __future__ import annotations

import re
from typing import Literal, Optional

from src.properties import BaseProperty, get_property_from_dict

from .base import BaseSchema

METHOD_NAME_REGEXP = re.compile(r"\w+\.(\w+)")


class MethodSchema(BaseSchema):
    name: str
    access_token_type: list[Literal["open", "user", "group", "service", "anonymous"]]
    parameters: list[BaseProperty]
    responses: list[str]
    errors: Optional[list[str]] = None

    @classmethod
    def from_dict(cls, data: dict) -> MethodSchema:
        name = parse_method_name(data["name"])
        access_token_type = data["access_token_type"]
        responses = parse_method_responses(data["responses"])

        parameters = []
        raw_parameters = data["parameters"].copy()
        for raw_parameter in raw_parameters:
            name_parameter = raw_parameter.pop("name")
            parameter = get_property_from_dict(raw_parameter, name_parameter)
            parameters.append(parameter)

        return cls(
            name=name,
            access_token_type=access_token_type,
            parameters=parameters,
            responses=responses,
        )


def parse_method_name(string: str) -> str:
    result = METHOD_NAME_REGEXP.match(string)
    if result is None:
        raise ValueError(f"Can't parse method name {string}")
    return result.group(1)


def parse_method_responses(responses: dict[str, dict]) -> list[str]:
    result = []
    for response in responses.values():
        result.append(response["$ref"])
    return result
