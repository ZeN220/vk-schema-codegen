import pytest

from src.fields import StringArrayItem

MINIMUM_DATA = {"type": "string"}
TEST_DATA = (MINIMUM_DATA, {**MINIMUM_DATA, "description": "test_description"})


class TestStringArrayItem:
    @pytest.mark.parametrize("data", TEST_DATA)
    @pytest.mark.parametrize("typehint", ["str"])
    def test_typehints(self, data: dict, typehint: str):
        field = StringArrayItem(**data)
        assert field.__typehint__ == typehint
