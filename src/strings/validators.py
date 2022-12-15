from __future__ import annotations

import keyword

from .reference import parse_reference


def validate_field(string: str) -> str:
    if string[0].isdigit():
        return f"_{string}"
    if keyword.iskeyword(string):
        return f"{string}_"
    return string


def validate_order_references(objects: dict) -> dict:
    """
    In code, some classes can be inherited from other classes,
    which are undefined at the moment. For this, this function orders references of
    classes in such a way that, inherited classes are defined after the classes they inherit from.
    :param objects: objects for which references are to be ordered
    :return:
    """
    result: dict[str, dict] = {}
    for name, schema in objects.items():
        schema_references = _get_references(schema)
        while schema_references:
            reference_name = schema_references[0]
            reference_object = objects[reference_name]
            object_references = _get_references(reference_object)
            if all(reference in result.keys() for reference in object_references):
                schema_references.pop(0)
                result[reference_name] = reference_object
                continue
            for reference in object_references:
                if reference not in result.keys():
                    schema_references.insert(0, reference)
        result[name] = schema
    return result


def _get_references(data: dict) -> list[str]:
    result = []

    all_of = data.get("allOf", [])
    one_of = data.get("oneOf", [])
    references: list[dict] = [*all_of, *one_of]
    if data.get("$ref") is not None:
        references.append(data)
    for item in references:
        reference = item.get("$ref")
        if reference is not None:
            reference = parse_reference(reference)
            result.append(reference)
    return result
