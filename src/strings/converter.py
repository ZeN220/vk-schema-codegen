from __future__ import annotations


def to_camel_case(snake_str: str) -> str:
    result = str()
    for word in snake_str.split("_"):
        result += word[0].upper() + word[1:]
    return result


def to_python_type(type_: str) -> str:
    if type_ == "string":
        return "str"
    elif type_ == "integer":
        return "int"
    elif type_ == "boolean":
        return "bool"
    raise ValueError(f"Unknown type: {type_}")


def to_python_types(types: list[str]) -> list[str]:
    result = []
    for type_ in types:
        result.append(to_python_type(type_))
    return result
