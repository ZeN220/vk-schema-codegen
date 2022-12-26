import pytest

from src.fields import UnionField

MINIMUM_DATA: dict = {"name": "test_name", "type": ["string", "integer"]}


class TestUnionField:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[typing.Union[str, int]] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: typing.Union[str, int]\n"),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                "    test_name: typing.Optional[typing.Union[str, int]] = None\n    "
                '"""Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = UnionField(**data)
        assert field.to_field_class() == expected
