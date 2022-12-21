import pytest

from src.fields import StringEnumField

MINIMUM_DATA: dict = {
    "__typehint__": "ObjectTestName",
    "name": "test_name",
    "type": "string",
    "enum": ["test_value"],
}
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "test_description"},
    {**MINIMUM_DATA, "required": True},
    {**MINIMUM_DATA, "enumNames": ["test_name"]},
]


class TestStringEnumProperty:
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
                    "    test_name: typing.Optional[ObjectTestName] = None\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = StringEnumField(**data)
        assert field.to_field_class() == expected
