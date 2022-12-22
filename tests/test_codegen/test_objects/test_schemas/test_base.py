import pytest

from src.codegen.objects.schemas import BaseSchema


def test_base_field_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseSchema(name="TestName").to_class()
