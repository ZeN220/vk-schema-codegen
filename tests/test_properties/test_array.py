import pytest

from src.properties import ArrayProperty, DictProperty

# For testing, need to create a fake class to use as the items class
MINIMUM_DATA: dict = {
    "name": "test_name",
    "type": "array",
    "items": DictProperty(name="test_name", type="dict"),
}


class TestArrayProperty:
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
                    "items": DictProperty(
                        name="test_name", type="dict", description="Item description"
                    ),
                },
                "    test_name: typing.Optional[list[dict]] = None\n"
                '    """\n    Description array item: Item description\n    """\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        property_ = ArrayProperty(**data)
        assert property_.to_field_class() == expected
