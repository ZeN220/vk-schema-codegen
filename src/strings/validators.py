import keyword


def validate_field(string: str) -> str:
    if string[0].isdigit():
        return f"_{string}"
    if keyword.iskeyword(string):
        return f"{string}_"
    return string
