import pytest

from src.properties import StringProperty

MINIMUM_DATA: dict = {"name": "test_name", "type": "string"}


class TestStringProperty:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[str] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: str\n"),
            (
                {**MINIMUM_DATA, "maxLength": 1},
                "    test_name: typing.Optional[str] = None\n"
                '    """\n    Max length: 1\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "format": "uri"},
                "    test_name: typing.Optional[str] = None\n"
                '    """\n    Format: uri\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                '    test_name: typing.Optional[str] = None\n    """Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        property_ = StringProperty(**data)
        assert property_.to_field_class() == expected
