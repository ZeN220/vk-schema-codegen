import pytest

from src.properties import IntegerProperty

MINIMUM_DATA: dict = {"name": "test_name", "type": "integer"}


class TestIntegerProperty:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[int] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: int\n"),
            ({**MINIMUM_DATA, "default": 1}, "    test_name: int = 1\n"),
            (
                {**MINIMUM_DATA, "minimum": 1},
                "    test_name: typing.Optional[int] = None\n"
                '    """\n    Minimum value: 1\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "maximum": 1},
                "    test_name: typing.Optional[int] = None\n"
                '    """\n    Maximum value: 1\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "entity": "owner"},
                "    test_name: typing.Optional[int] = None\n"
                '    """\n    Entity: owner\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "format": "int64"},
                "    test_name: typing.Optional[int] = None\n"
                '    """\n    Format: int64\n    """\n',
            ),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                '    test_name: typing.Optional[int] = None\n    """Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        property_ = IntegerProperty(**data)
        assert property_.to_field_class() == expected

    def test__get_default_field_class(self):
        property_ = IntegerProperty(default=1, **MINIMUM_DATA)
        assert property_._get_default_field_class() == "    test_name: int = 1\n"

    def test__get_default_field_class_with_alias(self):
        test_data = {"type": "integer", "name": "global", "default": 1}
        property_ = IntegerProperty(**test_data)
        assert property_._get_default_field_class() == (
            '    global_: int = pydantic.Field(\n        default=1, alias="global"\n    )\n'
        )

    def test__get_default_field_class_no_default(self):
        property_ = IntegerProperty(**MINIMUM_DATA)
        with pytest.raises(ValueError):
            property_._get_default_field_class()
