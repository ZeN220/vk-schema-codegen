import pytest

from src.properties import ReferenceProperty

MINIMUM_DATA: dict = {"name": "test_name", "reference": "Object"}


class TestReferenceProperty:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[Object] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: Object\n"),
            (
                {**MINIMUM_DATA, "default": "test_default"},
                "    test_name: Object = Object.TEST_DEFAULT\n",
            ),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                '    test_name: typing.Optional[Object] = None\n    """Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        property_ = ReferenceProperty(**data)
        assert property_.to_field_class() == expected

    def test__get_default_field_class(self):
        property_ = ReferenceProperty(default="test_default", **MINIMUM_DATA)
        assert property_._get_default_field_class() == (
            "    test_name: Object = Object.TEST_DEFAULT\n"
        )

    def test__get_default_field_class_with_alias(self):
        test_data = {
            "name": "global",
            "reference": "Object",
            "default": "test_default",
        }
        property_ = ReferenceProperty(**test_data)
        assert property_._get_default_field_class() == (
            "    global_: Object = pydantic.Field(\n"
            '        default=Object.TEST_DEFAULT, alias="global"\n'
            "    )\n"
        )

    def test__get_default_field_class_no_default(self):
        property_ = ReferenceProperty(**MINIMUM_DATA)
        with pytest.raises(ValueError):
            property_._get_default_field_class()
