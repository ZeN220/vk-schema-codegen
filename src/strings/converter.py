def to_camel_case(snake_str: str) -> str:
    result = str()
    for word in snake_str.split("_"):
        result += word[0].upper() + word[1:]
    return result


def to_python_types(types: list[str]) -> list[str]:
    result = []
    for type_field in types:
        if type_field == "string":
            result.append("str")
        elif type_field == "integer":
            result.append("int")
        else:
            raise ValueError(f"Unknown union type: {type_field}")
    return result
