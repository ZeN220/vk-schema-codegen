def to_camel_case(snake_str: str) -> str:
    result = snake_str.title().replace("_", "")
    return result
