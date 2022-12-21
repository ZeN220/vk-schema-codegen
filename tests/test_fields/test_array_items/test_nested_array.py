import pytest

from src.fields import NestedArrayItem, StringArrayItem


class TestNestedArrayItem:
    @pytest.mark.parametrize(
        "data, typehint",
        [
            ({"type": "array", "items": StringArrayItem({"type": "string"})}, "list[str]"),
        ],
    )
    def test_typehint(self, data: dict, typehint: str):
        item = NestedArrayItem(**data)
        assert item.__typehint__ == typehint
