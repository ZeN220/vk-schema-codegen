import pytest

from src.fields import PatternField, StringField

# For testing, need to create a fake class to use as the pattern properties
MINIMUM_DATA: dict = {
    "name": "test_name",
    "type": "object",
    "patternProperties": {"this_is_regexp": StringField(name="test_name", type="string")},
    "additionalProperties": False,
}

DEFAULT_DESCRIPTION = (
    "\n" "    Patterns of dict (as regexp) in the form of key-value:\n" "    this_is_regexp: str\n"
)
TEST_DATA = [
    MINIMUM_DATA,
    {**MINIMUM_DATA, "description": "Test description"},
    {**MINIMUM_DATA, "required": True},
]


class TestPatterField:
    @pytest.mark.parametrize(
        "data, expected",
        list(
            zip(
                TEST_DATA,
                [
                    (
                        f"    test_name: typing.Optional[dict[str, str]] = None\n"
                        f'    """{DEFAULT_DESCRIPTION}    """\n'
                    ),
                    (
                        f"    test_name: typing.Optional[dict[str, str]] = None\n"
                        f'    """\n    Test description{DEFAULT_DESCRIPTION}    """\n'
                    ),
                    ("    test_name: dict[str, str]\n" f'    """{DEFAULT_DESCRIPTION}    """\n'),
                ],
            )
        ),
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = PatternField(**data)
        assert field.to_field_class() == expected
