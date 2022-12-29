import pytest

from src.fields import FloatField

MINIMUM_DATA: dict = {"name": "test_name", "type": "float"}


class TestFloatField:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[float] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: float\n"),
            (
                {**MINIMUM_DATA, "minimum": 1.0},
                "    test_name: typing.Optional[float] = None\n"
                '    """\n    Minimum value: 1.0\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "minimum": 1},
                "    test_name: typing.Optional[float] = None\n"
                '    """\n    Minimum value: 1\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "maximum": 1},
                "    test_name: typing.Optional[float] = None\n"
                '    """\n    Maximum value: 1\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                '    test_name: typing.Optional[float] = None\n    """Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = FloatField(**data)
        assert field.to_field_class() == expected
