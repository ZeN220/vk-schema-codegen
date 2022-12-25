import pytest

from src.fields import BooleanField

MINIMUM_DATA: dict = {"name": "test_name", "type": "boolean"}
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "test_description"},
    {**MINIMUM_DATA, "required": True},
    {**MINIMUM_DATA, "default": True},
]


class TestBooleanField:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[bool] = None\n",
                    '    test_name: typing.Optional[bool] = None\n    """test_description"""\n',
                    "    test_name: bool\n",
                    "    test_name: bool = True\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = BooleanField(**data)
        assert field.to_field_class() == expected

    def test__get_default_field_class(self):
        field = BooleanField(default=True, **MINIMUM_DATA)
        assert field._get_default_field_class() == ("    test_name: bool = True\n")

    def test__get_default_field_class_with_alias(self):
        test_data = {"type": "boolean", "name": "global", "default": True}
        field = BooleanField(**test_data)
        assert field._get_default_field_class() == (
            "    global_: bool = pydantic.Field(\n"
            '        default=True, alias="global"\n'
            "    )\n"
        )

    def test__get_default_field_class_no_default(self):
        field = BooleanField(**MINIMUM_DATA)
        with pytest.raises(ValueError):
            field._get_default_field_class()
