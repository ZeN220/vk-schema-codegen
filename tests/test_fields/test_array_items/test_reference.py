import pytest

from src.fields import ReferenceArrayItem


class TestReferenceArrayItem:
    @pytest.mark.parametrize(
        "data, typehint",
        [
            ({"reference": "Object"}, "Object"),
        ],
    )
    def test_typehint(self, data: dict, typehint: str):
        field = ReferenceArrayItem(**data)
        assert field.__typehint__ == typehint
