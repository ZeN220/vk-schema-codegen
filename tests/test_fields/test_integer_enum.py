import pytest

from src.fields import IntegerEnumField

MINIMUM_DATA: dict = {
    "__typehint__": "ObjectTestName",
    "name": "test_name",
    "type": "integer",
    "enum": [1],
    "enumNames": ["test_name"],
}
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "test_description"},
    {**MINIMUM_DATA, "required": True},
]


class TestIntegerEnumProperty:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[ObjectTestName] = None\n",
                    # Very long line
                    (
                        "    test_name: typing.Optional[ObjectTestName] = None\n"
                        '    """test_description"""\n'
                    ),
                    "    test_name: ObjectTestName\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = IntegerEnumField(**data)
        assert field.to_field_class() == expected
