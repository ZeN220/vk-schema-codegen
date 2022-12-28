from __future__ import annotations

import pytest

from src.strings.converter import to_camel_case, to_python_type, to_python_types


class TestConverter:
    @pytest.mark.parametrize(
        "snake_str, expected",
        [
            ("snake_str", "SnakeStr"),
            ("snake_str_2", "SnakeStr2"),
            ("snakeStr", "SnakeStr"),
        ],
    )
    def test_to_camel_case(self, snake_str: str, expected: str):
        assert to_camel_case(snake_str) == expected

    @pytest.mark.parametrize(
        "type_field, expected",
        [
            ("string", "str"),
            ("integer", "int"),
            ("boolean", "bool"),
        ],
    )
    def test_to_python_type(self, type_field: str, expected: str):
        assert to_python_type(type_field) == expected

    def test_to_python_type_unknown(self):
        with pytest.raises(ValueError):
            to_python_type("unknown")

    @pytest.mark.parametrize(
        "types, expected",
        [
            (["string"], ["str"]),
            (["string", "integer"], ["str", "int"]),
            (["string", "boolean"], ["str", "bool"]),
        ],
    )
    def test_to_python_types(self, types: list[str], expected: list[str]):
        assert to_python_types(types) == expected
