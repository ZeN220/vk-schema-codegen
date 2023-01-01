import pytest

from src.properties import UnionProperty

MINIMUM_DATA: dict = {"name": "test_name", "type": ["string", "integer"]}


class TestUnionProperty:
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
        property_ = UnionProperty(**data)
        assert property_.to_field_class() == expected
