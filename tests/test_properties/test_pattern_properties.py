import pytest

from src.properties import IntegerProperty, PatternProperty, StringProperty

# For testing, need to create a fake class to use as the pattern properties
MINIMUM_DATA: dict = {
    "name": "test_name",
    "type": "object",
    "patternProperties": {"this_is_regexp": StringProperty(name="test_name", type="string")},
    "additionalProperties": False,
}

DEFAULT_DESCRIPTION = "\n    Patterns of dict keys (as regexp): this_is_regexp"


class TestPatternProperty:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (
                MINIMUM_DATA,
                f"    test_name: typing.Optional[dict[str, str]] = None\n"
                f'    """{DEFAULT_DESCRIPTION}\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "required": True},
                f"    test_name: dict[str, str]\n" f'    """{DEFAULT_DESCRIPTION}\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                f"    test_name: typing.Optional[dict[str, str]] = None\n"
                f'    """\n    Test description{DEFAULT_DESCRIPTION}\n    """\n',
            ),
            (
                {
                    **MINIMUM_DATA,
                    "patternProperties": {
                        "this_is_regexp": StringProperty(name="test_name", type="string"),
                        "this_is_regexp2": IntegerProperty(name="test_name2", type="integer"),
                    },
                },
                f"    test_name: typing.Optional[dict[str, typing.Union[str, int]]] = None\n"
                f'    """{DEFAULT_DESCRIPTION}, this_is_regexp2\n    """\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        property_ = PatternProperty(**data)
        assert property_.to_field_class() == expected
