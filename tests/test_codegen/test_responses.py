import json
from pathlib import Path

import pytest

from src.codegen.responses import (
    ResponseSection,
    generate_classes,
    generate_responses,
    get_responses,
    parse_responses,
)
from src.schemas import ObjectSchema, ResponseSchema
from src.schemas.enum import EnumStringSchema, get_enum_from_dict


def create_response_file(tmp_path: Path, response: dict):
    response_path = tmp_path / "responses.json"
    with response_path.open("w", encoding="utf-8") as response_file:
        json.dump({"definitions": response}, response_file)
    return response_path


def test_get_responses(tmp_path_factory: pytest.TempPathFactory):
    test_response: dict[str, dict] = {
        "test_response": {"type": "object", "properties": {"response": {"type": "integer"}}}
    }
    temp_directory = tmp_path_factory.mktemp("data")
    section_path = temp_directory / "section"
    path_without_responses = temp_directory / "another_section"
    section_path.mkdir()
    path_without_responses.mkdir()
    create_response_file(section_path, test_response)
    test_response_schema = ResponseSchema.from_dict(
        "TestResponse", test_response["test_response"]["properties"]["response"]
    )
    section = ResponseSection(name="section", responses=[test_response_schema], imports=set())
    assert get_responses(temp_directory) == [section]


def test_parse_responses():
    test_schemas = {
        "test_response": {
            "type": "object",
            "properties": {"response": {"type": "integer"}},
        },
        "test_response_2": {
            "type": "object",
            "properties": {
                "response": {"type": "object", "properties": {"test": {"type": "string"}}}
            },
        },
        "test_response_3": {
            "type": "object",
            "properties": {
                "response": {
                    "type": "string",
                    "enum": ["test", "test2"],
                    "required": True,
                }
            },
        },
    }
    response_schema = ResponseSchema.from_dict(
        "TestResponse", test_schemas["test_response"]["properties"]["response"]
    )

    test_response_2 = test_schemas["test_response_2"]["properties"]["response"]
    object_2_schema = ObjectSchema.from_dict("TestResponse2Model", test_response_2["properties"])
    response_2_schema = ResponseSchema.from_dict("TestResponse2", test_response_2)

    test_response_3 = test_schemas["test_response_3"]["properties"]["response"]
    response_3_schema = ResponseSchema.from_dict("TestResponse3", test_response_3)
    enum_3_schema = EnumStringSchema(
        name="TestResponse3Model",
        type="string",
        enum=test_response_3["enum"],
        enumNames=test_response_3["enum"],
    )
    assert parse_responses(test_schemas) == [
        response_schema,
        object_2_schema,
        response_2_schema,
        enum_3_schema,
        response_3_schema,
    ]


def test_generate_classes(tmp_path):
    output = tmp_path / "path" / "to" / "output"
    test_schema = ResponseSchema.from_dict("TestResponse", {"type": "integer"})
    test_section = ResponseSection(name="section", responses=[test_schema], imports=set())
    test_schema_2 = get_enum_from_dict(
        "TestResponse2", {"type": "string", "enum": ["test", "test2"]}
    )
    test_section_2 = ResponseSection(
        name="section_2", responses=[test_schema_2], imports=["TestObjectImport"]
    )

    generate_classes([test_section, test_section_2], output, "package")

    section_path = output / "section.py"
    section_2_path = output / "section_2.py"
    assert section_path.exists()
    assert section_2_path.exists()
    assert section_path.read_text() == (
        f"from __future__ import annotations\n\n"
        f"import typing\n\n"
        f"import pydantic\n\n\n"
        f"{test_schema.to_class()[:-1]}"
    )
    assert section_2_path.read_text() == (
        f"from __future__ import annotations\n\n"
        f"import enum\n\n"
        f"import pydantic\n\n"
        f"from package.objects import (\n"
        f"    TestObjectImport,\n"
        f")\n\n\n"
        f"{test_schema_2.to_class()[:-1]}"
    )


def test_generate_responses(tmp_path_factory: pytest.TempPathFactory):
    test_response = {
        "test_response": {"type": "object", "properties": {"response": {"type": "integer"}}}
    }
    output_path = tmp_path_factory.mktemp("output")
    responses_path = tmp_path_factory.mktemp("data")
    section_path = responses_path / "section"

    section_path.mkdir()
    create_response_file(section_path, test_response)

    generate_responses(responses_path, output_path, "package")
