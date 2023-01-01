import pytest

from src.properties import StringEnumProperty

MINIMUM_DATA: dict = {
    "__typehint__": "ObjectTestName",
    "name": "test_name",
    "type": "string",
    "enum": ["test_value"],
}
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "Test description"},
    {**MINIMUM_DATA, "required": True},
    {**MINIMUM_DATA, "enumNames": ["test_name"]},
]


class TestStringEnumProperty:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[ObjectTestName] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: ObjectTestName\n"),
            (
                {**MINIMUM_DATA, "enumNames": ["test_name"]},
                "    test_name: typing.Optional[ObjectTestName] = None\n",
            ),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                "    test_name: typing.Optional[ObjectTestName] = None\n"
                '    """Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        property_ = StringEnumProperty(**data)
        assert property_.to_field_class() == expected
