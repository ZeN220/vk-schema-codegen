import pytest

from src.fields import DictField

MINIMUM_DATA: dict = {"name": "test_name", "type": "dict"}


class TestDictField:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[dict] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: dict\n"),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                '    test_name: typing.Optional[dict] = None\n    """Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = DictField(**data)
        assert field.to_field_class() == expected
