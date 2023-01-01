import pytest

from src.properties import BooleanProperty

MINIMUM_DATA: dict = {"name": "test_name", "type": "boolean"}


class TestBooleanProperty:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (MINIMUM_DATA, "    test_name: typing.Optional[bool] = None\n"),
            ({**MINIMUM_DATA, "required": True}, "    test_name: bool\n"),
            ({**MINIMUM_DATA, "default": True}, "    test_name: bool = True\n"),
            ({**MINIMUM_DATA, "default": 1}, "    test_name: bool = True\n"),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                '    test_name: typing.Optional[bool] = None\n    """Test description"""\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        property_ = BooleanProperty(**data)
        assert property_.to_field_class() == expected

    def test__get_default_field_class(self):
        property_ = BooleanProperty(default=True, **MINIMUM_DATA)
        assert property_._get_default_field_class() == "    test_name: bool = True\n"

    def test__get_default_field_class_with_alias(self):
        test_data = {"type": "boolean", "name": "global", "default": True}
        property_ = BooleanProperty(**test_data)
        assert property_._get_default_field_class() == (
            "    global_: bool = pydantic.Field(\n"
            '        default=True, alias="global"\n'
            "    )\n"
        )

    def test__get_default_field_class_no_default(self):
        property_ = BooleanProperty(**MINIMUM_DATA)
        with pytest.raises(ValueError):
            property_._get_default_field_class()
