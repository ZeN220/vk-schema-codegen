import pytest

from src.fields import FloatField

MINIMUM_DATA: dict = {"name": "test_name", "type": "float"}
TEST_DATA = (
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "Test description"},
    {**MINIMUM_DATA, "required": True},
    {**MINIMUM_DATA, "minimum": 1.0},
    {**MINIMUM_DATA, "minimum": 1},
    {**MINIMUM_DATA, "maximum": 1},
)


class TestFloatField:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[float] = None\n",
                    '    test_name: typing.Optional[float] = None\n    """Test description"""\n',
                    "    test_name: float\n",
                    "    test_name: typing.Optional[float] = None\n",
                    "    test_name: typing.Optional[float] = None\n",
                    "    test_name: typing.Optional[float] = None\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = FloatField(**data)
        assert field.to_field_class() == expected
