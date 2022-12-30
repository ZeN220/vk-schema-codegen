import pytest

from src.properties import DictProperty

MINIMUM_DATA: dict = {"name": "test_name", "type": "dict"}


class TestDictProperty:
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
        property_ = DictProperty(**data)
        assert property_.to_field_class() == expected
