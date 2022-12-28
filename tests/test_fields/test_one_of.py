import pytest

from src.fields import OneOfField, ReferenceField, StringField

# For testing, need to create a fake classes to use as the oneOf list
MINIMUM_DATA: dict = {
    "name": "test_name",
    "oneOf": [
        StringField(name="test_name", type="string"),
        ReferenceField(name="test_name", reference="Object"),
    ],
}


class TestOneOfField:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[typing.Union[str, Object]] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: typing.Union[str, Object]\n"),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                "    test_name: typing.Optional[typing.Union[str, Object]] = None\n    "
                '"""Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = OneOfField(**data)
        assert field.to_field_class() == expected
