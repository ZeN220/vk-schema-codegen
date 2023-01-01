import pytest

from src.schemas import BaseSchema


def test_base_schema_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseSchema(name="TestName").to_class()
