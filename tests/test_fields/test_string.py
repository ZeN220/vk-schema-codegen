import pytest

from src.fields import StringField

MINIMUM_DATA: dict = {"name": "test_name", "type": "string"}


class TestStringField:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[str] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: str\n"),
            ({**MINIMUM_DATA, "maxLength": 1}, "    test_name: typing.Optional[str] = None\n"),
            ({**MINIMUM_DATA, "format": "uri"}, "    test_name: typing.Optional[str] = None\n"),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                '    test_name: typing.Optional[str] = None\n    """Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = StringField(**data)
        assert field.to_field_class() == expected
