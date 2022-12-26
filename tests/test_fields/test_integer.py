import pytest

from src.fields import IntegerField

MINIMUM_DATA: dict = {"name": "test_name", "type": "integer"}


class TestIntegerField:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[int] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: int\n"),
            ({**MINIMUM_DATA, "default": 1}, "    test_name: int = 1\n"),
            ({**MINIMUM_DATA, "minimum": 1}, "    test_name: typing.Optional[int] = None\n"),
            ({**MINIMUM_DATA, "maximum": 1}, "    test_name: typing.Optional[int] = None\n"),
            ({**MINIMUM_DATA, "entity": "owner"}, "    test_name: typing.Optional[int] = None\n"),
            ({**MINIMUM_DATA, "format": "int64"}, "    test_name: typing.Optional[int] = None\n"),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                '    test_name: typing.Optional[int] = None\n    """Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = IntegerField(**data)
        assert field.to_field_class() == expected

    def test__get_default_field_class(self):
        field = IntegerField(default=1, **MINIMUM_DATA)
        assert field._get_default_field_class() == "    test_name: int = 1\n"

    def test__get_default_field_class_with_alias(self):
        test_data = {"type": "integer", "name": "global", "default": 1}
        field = IntegerField(**test_data)
        assert field._get_default_field_class() == (
            '    global_: int = pydantic.Field(\n        default=1, alias="global"\n    )\n'
        )

    def test__get_default_field_class_no_default(self):
        field = IntegerField(**MINIMUM_DATA)
        with pytest.raises(ValueError):
            field._get_default_field_class()
