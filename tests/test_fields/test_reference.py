import pytest

from src.fields import ReferenceField

MINIMUM_DATA: dict = {"name": "test_name", "reference": "Object"}
TEST_DATA = (
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "test_description"},
    {**MINIMUM_DATA, "required": True},
    {**MINIMUM_DATA, "default": "test_default"},
)


class TestReferenceField:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[Object] = None\n",
                    '    test_name: typing.Optional[Object] = None\n    """test_description"""\n',
                    "    test_name: Object\n",
                    "    test_name: Object = Object.TEST_DEFAULT\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = ReferenceField(**data)
        assert field.to_field_class() == expected

    def test__get_default_field_class(self):
        field = ReferenceField(default="test_default", **MINIMUM_DATA)
        assert field._get_default_field_class() == (
            "    test_name: Object = Object.TEST_DEFAULT\n"
        )

    def test__get_default_field_class_with_alias(self):
        test_data = {
            "name": "global",
            "reference": "Object",
            "default": "test_default",
        }
        field = ReferenceField(**test_data)
        assert field._get_default_field_class() == (
            "    global_: Object = pydantic.Field(\n"
            '        default=Object.TEST_DEFAULT, alias="global"\n'
            "    )\n"
        )

    def test__get_default_field_class_no_default(self):
        field = ReferenceField(**MINIMUM_DATA)
        with pytest.raises(ValueError):
            field._get_default_field_class()
