import pytest

from src.fields import DictField

MINIMUM_DATA: dict = {"name": "test_name", "type": "dict"}
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "Test description"},
    {**MINIMUM_DATA, "required": True},
]


class TestDictField:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[dict] = None\n",
                    '    test_name: typing.Optional[dict] = None\n    """Test description"""\n',
                    "    test_name: dict\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = DictField(**data)
        assert field.to_field_class() == expected
