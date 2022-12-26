import pytest

from src.fields import ArrayField, DictField

# For testing, need to create a fake class to use as the items class
MINIMUM_DATA: dict = {
    "name": "test_name",
    "type": "array",
    "items": DictField(name="test_name", type="dict"),
}


class TestArrayField:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[list[dict]] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: list[dict]\n"),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                '    test_name: typing.Optional[list[dict]] = None\n    """Test description"""\n',
            ),
            (
                {
                    **MINIMUM_DATA,
                    "items": DictField(
                        name="test_name", type="dict", description="Item description"
                    ),
                },
                '    test_name: typing.Optional[list[dict]] = None\n    """Item description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = ArrayField(**data)
        assert field.to_field_class() == expected
