from typing import Type

import pytest

from src.fields import BaseField


def get_implemented_class() -> Type[BaseField]:
    class ImplementedClass(BaseField):
        @property
        def __typehint__(self) -> str:
            return "str"

    return ImplementedClass


class TestBaseField:
    def test_base_field_not_implemented(self):
        with pytest.raises(NotImplementedError):
            BaseField(name="test_name", type="string").__typehint__  # noqa

    def test__get_required_field_class(self):
        field_class = get_implemented_class()
        field = field_class(name="test_name", type="string", required=True)
        assert field._get_required_field_class() == "    test_name: str\n"

    def test__get_required_field_class_with_alias(self):
        field_class = get_implemented_class()
        field = field_class(name="global", type="string", required=True)
        assert field._get_required_field_class() == (
            "    global_: str = pydantic.Field(\n" '        alias="global"\n' "    )\n"
        )

    def test__get_required_field_class_no_required(self):
        field_class = get_implemented_class()
        field = field_class(name="test_name", type="string", required=False)
        with pytest.raises(ValueError):
            field._get_required_field_class()

    def test__get_optional_field_class(self):
        field_class = get_implemented_class()
        field = field_class(name="test_name", type="string", required=False)
        assert field._get_optional_field_class() == "    test_name: typing.Optional[str] = None\n"

    def test__get_optional_field_class_with_alias(self):
        field_class = get_implemented_class()
        field = field_class(name="global", type="string", required=False)
        assert field._get_optional_field_class() == (
            "    global_: typing.Optional[str] = pydantic.Field(\n"
            '        default=None, alias="global"\n'
            "    )\n"
        )

    def test__get_optional_field_class_no_optional(self):
        field_class = get_implemented_class()
        field = field_class(name="test_name", type="string", required=True)
        with pytest.raises(ValueError):
            field._get_optional_field_class()
