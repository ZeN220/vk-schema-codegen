from __future__ import annotations

import keyword


def is_valid_name(string: str) -> bool:
    return not (string[0].isdigit() or keyword.iskeyword(string))


def validate_name(string: str) -> str:
    if string[0].isdigit():
        return f"_{string}"
    if keyword.iskeyword(string):
        return f"{string}_"
    return string
