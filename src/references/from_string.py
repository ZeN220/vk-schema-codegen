import re

from src.strings import to_camel_case

REFERENCE_REGEX = re.compile(r"\.\./[a-zA-Z]+/objects\.json#/definitions/([a-zA-Z_]+)")


def parse_reference(reference: str) -> str:
    result = REFERENCE_REGEX.match(reference)
    if result is None:
        raise ValueError(f"Invalid reference: {result}")
    return result.group(1)


def get_reference(reference: str) -> str:
    reference = parse_reference(reference)
    return to_camel_case(reference)
