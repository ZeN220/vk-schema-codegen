import re
from typing import Optional

from .converter import to_camel_case

REFERENCE_REGEX = re.compile(r"\.\./[a-zA-Z]+/objects\.json#/definitions/([a-zA-Z_]+)")


def parse_reference(reference: str) -> str:
    result = REFERENCE_REGEX.match(reference)
    if result is None:
        raise ValueError(f"Invalid reference: {result}")
    return result.group(1)


def get_reference(reference: str) -> str:
    reference = parse_reference(reference)
    return to_camel_case(reference)


def parse_responses_references(responses: dict[str, dict]) -> set[str]:
    references = []
    for response in responses.values():
        response = response["properties"]["response"]
        ref = response.get("$ref")
        if ref is not None:
            references.append(get_reference(ref))
            continue
        if response.get("type") == "array":
            ref = _get_reference_from_array(response)
            if ref is not None:
                references.append(ref)
        if response.get("type") == "object":
            properties = response.get("properties")
            if properties is None:
                properties = response["patternProperties"]
            references_from_properties = _get_references_from_properties(properties)
            references.extend(references_from_properties)
    return set(references)


def _get_reference_from_array(array: dict) -> Optional[str]:
    array_item = array["items"]
    ref = array_item.get("$ref")
    if ref is not None:
        return get_reference(ref)

    item_type = array_item.get("type")
    while item_type == "array":
        nested_array = array_item["items"]
        ref = nested_array.get("$ref")
        if ref is not None:
            return get_reference(ref)
        item_type = nested_array.get("type")
        array_item = nested_array
    return None


def _get_references_from_properties(properties: dict[str, dict]) -> list[str]:
    references = []
    for property_ in properties.values():
        if property_.get("type") == "array":
            ref = _get_reference_from_array(property_)
            if ref is not None:
                references.append(ref)
            continue
        ref = property_.get("$ref")
        if ref is not None:
            references.append(get_reference(ref))
    return references
