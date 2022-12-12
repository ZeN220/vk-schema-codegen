import re

from .converter import to_camel_case

REFERENCE_REGEX = re.compile(r"\.\./[a-zA-Z]+/objects\.json#/definitions/([a-zA-Z_]+)")


def get_reference(reference: str) -> str:
    result = REFERENCE_REGEX.match(reference)
    if result is None:
        raise ValueError(f"Invalid reference: {result}")
    return to_camel_case(result.group(1))
