import pytest

from src.fields import UnionArrayItem


class TestUnionArrayItem:
    @pytest.mark.parametrize(
        "data, typehint", [({"type": ["string", "integer"]}, "typing.Union[str, int]")]
    )
    def test_typehint(self, data: dict, typehint: str):
        field = UnionArrayItem(**data)
        assert field.__typehint__ == typehint
