from typing import Type

import pytest

from src.properties import BaseProperty


def get_implemented_class() -> Type[BaseProperty]:
    class ImplementedClass(BaseProperty):
        @property
        def __typehint__(self) -> str:
            return "str"

    return ImplementedClass


class TestBaseProperty:
    def test_base_field_not_implemented(self):
        with pytest.raises(NotImplementedError):
            BaseProperty(name="test_name", type="string").__typehint__  # noqa

    def test__get_required_field_class(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string", required=True)
        assert property_._get_required_field_class() == "    test_name: str\n"

    def test__get_required_field_class_with_alias(self):
        property_class = get_implemented_class()
        property_ = property_class(name="global", type="string", required=True)
        assert property_._get_required_field_class() == (
            "    global_: str = pydantic.Field(\n" '        alias="global"\n' "    )\n"
        )

    def test__get_required_field_class_no_required(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string", required=False)
        with pytest.raises(ValueError):
            property_._get_required_field_class()

    def test__get_optional_field_class(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string", required=False)
        assert (
            property_._get_optional_field_class() == "    test_name: typing.Optional[str] = None\n"
        )

    def test__get_optional_field_class_with_alias(self):
        property_class = get_implemented_class()
        property_ = property_class(name="global", type="string", required=False)
        assert property_._get_optional_field_class() == (
            "    global_: typing.Optional[str] = pydantic.Field(\n"
            '        default=None, alias="global"\n'
            "    )\n"
        )

    def test__get_optional_field_class_no_optional(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string", required=True)
        with pytest.raises(ValueError):
            property_._get_optional_field_class()

    def test__get_description(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string", description="Test description")
        assert property_._get_description() == {"description": "Test description"}

    def test__get_description_empty(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string")
        assert property_._get_description() == {}

    def test__get_description_field_class(self):
        class DescriptionClass(BaseProperty):
            @property
            def __typehint__(self) -> str:
                return "str"

            def _get_description(self) -> dict:
                return {"description": "Test description", "another": "Test another"}

        property_ = DescriptionClass(name="test_name", type="string")
        assert property_._get_description_field_class() == (
            '    """\n    Test description\n    another: Test another\n    """\n'
        )

    def test__get_description_field_class_only_description(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string", description="Test description")
        assert property_._get_description_field_class() == '    """Test description"""\n'

    def test__get_description_field_class_empty(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string")
        assert property_._get_description_field_class() == ""

    def test_to_field_class_required(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string", required=True)
        assert property_.to_field_class() == "    test_name: str\n"

    def test_to_field_class_no_required(self):
        property_class = get_implemented_class()
        property_ = property_class(name="test_name", type="string")
        assert property_.to_field_class() == "    test_name: typing.Optional[str] = None\n"
