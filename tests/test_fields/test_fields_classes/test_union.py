import pytest

from src.fields import UnionField

MINIMUM_DATA: dict = {"name": "test_name", "type": ["string", "integer"]}
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "test_description"},
    {**MINIMUM_DATA, "required": True},
]


class TestUnionField:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    "    test_name: typing.Optional[typing.Union[str, int]] = None\n",
                    # Very long line
                    "    test_name: typing.Optional[typing.Union[str, int]] = None\n    "
                    '"""test_description"""\n',
                    "    test_name: typing.Union[str, int]\n",
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = UnionField(**data)
        assert field.to_field_class() == expected
