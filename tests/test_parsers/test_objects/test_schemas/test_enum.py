import pytest

from src.parsers.objects.schemas.enum import (
    EnumIntegerSchema,
    EnumSchema,
    EnumStringSchema,
    get_enum_from_dict,
    get_enums_from_all_of,
    get_enums_from_object,
)


def test_enum_schema_not_implemented():
    with pytest.raises(NotImplementedError):
        EnumSchema(name="TestName", type="string").to_class()


class TestEnumStringSchema:
    def test_to_class(self):
        enum = EnumStringSchema(
            type="string",
            name="TestName",
            description="Test description",
            enum=["value", "another_value"],
            enumNames=["name", "another name"],
        )
        class_string = enum.to_class()
        assert class_string == (
            "class TestName(enum.Enum):\n"
            '    """Test description"""\n\n'
            '    NAME = "value"\n'
            '    ANOTHER_NAME = "another_value"\n\n'
        )

    def test_to_class_without_enum_names(self):
        enum = EnumStringSchema(
            type="string",
            name="TestName",
            description="Test description",
            enum=["name", "another_name"],
        )
        class_string = enum.to_class()
        assert class_string == (
            "class TestName(enum.Enum):\n"
            '    """Test description"""\n\n'
            '    NAME = "name"\n'
            '    ANOTHER_NAME = "another_name"\n\n'
        )


class TestEnumIntegerSchema:
    def test_to_class(self):
        enum = EnumIntegerSchema(
            type="integer",
            name="TestName",
            description="Test description",
            enum=[1, 2],
            enumNames=["name", "another name"],
        )
        class_string = enum.to_class()
        assert class_string == (
            "class TestName(enum.IntEnum):\n"
            '    """Test description"""\n\n'
            "    NAME = 1\n"
            "    ANOTHER_NAME = 2\n\n"
        )


@pytest.mark.parametrize(
    "enum_data, expected_enum",
    [
        (
            {
                "type": "string",
                "description": "Test description",
                "enum": ["value", "another_value"],
                "enumNames": ["name", "another name"],
            },
            EnumStringSchema(
                type="string",
                name="TestName",
                description="Test description",
                enum=["value", "another_value"],
                enumNames=["name", "another name"],
            ),
        ),
        (
            {
                "type": "integer",
                "description": "Test description",
                "enum": [1, 2],
                "enumNames": ["name", "another name"],
            },
            EnumIntegerSchema(
                type="integer",
                name="TestName",
                description="Test description",
                enum=[1, 2],
                enumNames=["name", "another name"],
            ),
        ),
    ],
)
def test_get_enum_from_dict(enum_data: dict, expected_enum: EnumSchema):
    enum = get_enum_from_dict("TestName", enum_data)
    assert enum == expected_enum


def test_get_enum_from_dict_unknown_type():
    with pytest.raises(ValueError):
        get_enum_from_dict("TestName", {"type": "invalid_type", "enum": ["value"]})


@pytest.mark.parametrize(
    "object_name, object_data, expected_enums",
    [
        (
            "TestName",
            {
                "no_enum": {"type": "bool"},
                "test": {
                    "type": "string",
                    "description": "Test description",
                    "enum": ["value", "another_value"],
                },
                "another_test": {
                    "type": "integer",
                    "description": "Test description",
                    "enum": [1, 2],
                    "enumNames": ["name", "another name"],
                },
            },
            [
                EnumStringSchema(
                    type="string",
                    name="TestNameTest",
                    description="Test description",
                    enum=["value", "another_value"],
                    # Function get_enum_from_dict adds enumNames by values from enum
                    enumNames=["value", "another_value"],
                ),
                EnumIntegerSchema(
                    type="integer",
                    name="TestNameAnotherTest",
                    description="Test description",
                    enum=[1, 2],
                    enumNames=["name", "another name"],
                ),
            ],
        ),
        (
            "TestName",
            {},
            [],
        ),
    ],
)
def test_get_enums_from_object(
    object_name: str, object_data: dict, expected_enums: list[EnumSchema]
):
    enums = get_enums_from_object(object_name, object_data)
    assert enums == expected_enums


@pytest.mark.parametrize(
    "object_name, object_data, expected_enums",
    [
        (
            "TestName",
            [
                {"$ref": "../dir/objects.json#/definitions/object"},
                {
                    "type": "object",
                    "properties": {
                        "test": {
                            "type": "string",
                            "description": "Test description",
                            "enum": ["value", "another_value"],
                        }
                    },
                },
            ],
            [
                EnumStringSchema(
                    type="string",
                    name="TestNameTest",
                    description="Test description",
                    enum=["value", "another_value"],
                    # Function get_enum_from_dict adds enumNames by values from enum
                    enumNames=["value", "another_value"],
                )
            ],
        ),
    ],
)
def test_get_enums_from_all_of(
    object_name: str, object_data: list[dict], expected_enums: list[EnumSchema]
):
    enums = get_enums_from_all_of(object_name, object_data)
    assert enums == expected_enums
