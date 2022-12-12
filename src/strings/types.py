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
