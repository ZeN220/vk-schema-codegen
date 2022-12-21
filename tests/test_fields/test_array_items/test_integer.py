import pytest

from src.fields import IntegerArrayItem

MINIMUM_DATA: dict = {"type": "integer"}
TEST_DATA = (
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "test_description"},
    {**MINIMUM_DATA, "default": 1},
    {**MINIMUM_DATA, "minimum": 1},
    {**MINIMUM_DATA, "maximum": 1},
    {**MINIMUM_DATA, "entity": "owner"},
    {**MINIMUM_DATA, "format": "int64"},
)


class TestIntegerArrayItem:
    @pytest.mark.parametrize("data", TEST_DATA)
    @pytest.mark.parametrize("typehint", ["int"])
    def test_typehint(self, data: dict, typehint: str):
        field = IntegerArrayItem(**data)
        assert field.__typehint__ == typehint
