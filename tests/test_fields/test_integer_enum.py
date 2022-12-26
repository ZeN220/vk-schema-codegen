import pytest

from src.fields import IntegerEnumField

MINIMUM_DATA: dict = {
    "__typehint__": "ObjectTestName",
    "name": "test_name",
    "type": "integer",
    "enum": [1],
    "enumNames": ["test_name"],
}
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "Test description"},
    {**MINIMUM_DATA, "required": True},
    {**MINIMUM_DATA, "default": 1},
]


class TestIntegerEnumProperty:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[ObjectTestName] = None\n",
                    # Very long line
                    (
                        "    test_name: typing.Optional[ObjectTestName] = None\n"
                        '    """Test description"""\n'
                    ),
                    "    test_name: ObjectTestName\n",
                    "    test_name: ObjectTestName = ObjectTestName.TEST_NAME\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = IntegerEnumField(**data)
        assert field.to_field_class() == expected

    def test__get_default_field_class(self):
        field = IntegerEnumField(default=1, **MINIMUM_DATA)
        assert field._get_default_field_class() == (
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
        field = IntegerEnumField(**test_data)
        assert field._get_default_field_class() == (
            "    global_: ObjectTestName = pydantic.Field(\n"
            '        default=ObjectTestName.TEST_NAME, alias="global"\n'
            "    )\n"
        )

    def test__get_default_field_class_no_default(self):
        field = IntegerEnumField(**MINIMUM_DATA)
        with pytest.raises(ValueError):
            field._get_default_field_class()

    def test__get_default_enum_undefined(self):
        field = IntegerEnumField(default=123, **MINIMUM_DATA)
        with pytest.raises(ValueError):
            field._get_default_enum()
