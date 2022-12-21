import pytest

from src.fields import StringField

MINIMUM_DATA: dict = {"name": "test_name", "type": "string"}
TEST_DATA = (
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "test_description"},
    {**MINIMUM_DATA, "required": True},
    {**MINIMUM_DATA, "maxLength": 1},
    {**MINIMUM_DATA, "format": "uri"},
)


class TestStringField:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[str] = None\n",
                    '    test_name: typing.Optional[str] = None\n    """test_description"""\n',
                    "    test_name: str\n",
                    "    test_name: typing.Optional[str] = None\n",
                    "    test_name: typing.Optional[str] = None\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = StringField(**data)
        assert field.to_field_class() == expected
