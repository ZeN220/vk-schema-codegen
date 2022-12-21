import pytest

from src.fields import ArrayField, DictField

# For testing, need to create a fake class to use as the items class
MINIMUM_DATA: dict = {
    "name": "test_name",
    "type": "array",
    "items": DictField(name="test_name", type="dict"),
}
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "test_description"},
    {**MINIMUM_DATA, "required": True},
]


class TestArrayField:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[list[dict]] = None\n",
                    # Very long line
                    (
                        "    test_name: typing.Optional[list[dict]] = None\n"
                        '    """test_description"""\n'
                    ),
                    "    test_name: list[dict]\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = ArrayField(**data)
        assert field.to_field_class() == expected
