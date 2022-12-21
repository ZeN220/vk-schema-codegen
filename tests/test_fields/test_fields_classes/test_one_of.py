import pytest

from src.fields import OneOfField, ReferenceField, StringField

# For testing, need to create a fake classes to use as the oneOf list
MINIMUM_DATA: dict = {
    "name": "test_name",
    "oneOf": [
        StringField(name="test_name", type="string"),
        ReferenceField(name="test_name", reference="../dir/objects.json#/definitions/object"),
    ],
}
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "test_description"},
    {**MINIMUM_DATA, "required": True},
]


class TestOneOfField:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[typing.Union[str, Object]] = None\n",
                    # Very long line
                    "    test_name: typing.Optional[typing.Union[str, Object]] = None\n    "
                    '"""test_description"""\n',
                    "    test_name: typing.Union[str, Object]\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = OneOfField(**data)
        assert field.to_field_class() == expected
