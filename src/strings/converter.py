def to_camel_case(snake_str: str) -> str:
    result = str()
    for word in snake_str.split("_"):
        result += word[0].upper() + word[1:]
    return result
