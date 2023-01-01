import pytest

from src.properties import IntegerEnumProperty

MINIMUM_DATA: dict = {
    "__typehint__": "ObjectTestName",
    "name": "test_name",
    "type": "integer",
    "enum": [1],
    "enumNames": ["test_name"],
}


class TestIntegerEnumProperty:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[ObjectTestName] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: ObjectTestName\n"),
            (
                {**MINIMUM_DATA, "default": 1},
                "    test_name: ObjectTestName = ObjectTestName.TEST_NAME\n",
            ),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                (
                    "    test_name: typing.Optional[ObjectTestName] = None\n"
                    '    """Test description"""\n'
                ),
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        property_ = IntegerEnumProperty(**data)
        assert property_.to_field_class() == expected

    def test__get_default_field_class(self):
        property_ = IntegerEnumProperty(default=1, **MINIMUM_DATA)
        assert property_._get_default_field_class() == (
            "    test_name: ObjectTestName = ObjectTestName.TEST_NAME\n"
        )

    def test__get_default_field_class_with_alias(self):
        test_data = {
            "__typehint__": "ObjectTestName",
            "name": "global",
            "type": "integer",
            "enum": [1],
            "enumNames": ["test_name"],
            "default": 1,
        }
        property_ = IntegerEnumProperty(**test_data)
        assert property_._get_default_field_class() == (
            "    global_: ObjectTestName = pydantic.Field(\n"
            '        default=ObjectTestName.TEST_NAME, alias="global"\n'
            "    )\n"
        )

    def test__get_default_field_class_no_default(self):
        property_ = IntegerEnumProperty(**MINIMUM_DATA)
        with pytest.raises(ValueError):
            property_._get_default_field_class()

    def test__get_default_enum_undefined(self):
        property_ = IntegerEnumProperty(default=123, **MINIMUM_DATA)
        with pytest.raises(ValueError):
            property_._get_default_enum()
