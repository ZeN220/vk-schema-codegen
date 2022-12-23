import json
from pathlib import Path

import pytest

from src.codegen.objects.generator import (
    IMPORTS,
    generate_classes,
    generate_objects,
    get_objects,
    parse_objects,
)
from src.schemas import (
    AllOfSchema,
    ArraySchema,
    BoolSchema,
    ObjectSchema,
    OneOfSchema,
    ReferenceSchema,
)
from src.schemas.enum import get_enum_from_dict


def create_objects_file(tmp_path: Path, objects: dict):
    objects_path = tmp_path / "objects.json"
    with objects_path.open("w", encoding="utf-8") as objects_file:
        json.dump({"definitions": objects}, objects_file)
    return objects_path


def test_get_objects(tmp_path_factory: pytest.TempPathFactory):
    test_object = {
        "test_object": {"type": "object", "properties": {"test_property": {"type": "string"}}}
    }
    test_another_object = {
        "test_another_object": {
            "type": "object",
            "properties": {"test_another_property": {"type": "string"}},
        }
    }

    # Create a temporary directories
    # of the form /data/section/objects.json & /data/another_section/objects.json
    objects_path = tmp_path_factory.mktemp("data")
    section_path = objects_path / "section"
    another_section_path = objects_path / "another_section"
    path_without_objects = objects_path / "without_objects"
    section_path.mkdir()
    another_section_path.mkdir()
    path_without_objects.mkdir()

    create_objects_file(section_path, test_object)
    create_objects_file(another_section_path, test_another_object)

    assert get_objects(objects_path) == {**test_object, **test_another_object}


def test_parse_objects():
    test_object = {"type": "object", "properties": {"test_property": {"type": "string"}}}
    test_reference = {"$ref": "../dir/objects.json#/definitions/test_object"}
    test_array = {
        "type": "array",
        "items": {"type": "array", "items": {"$ref": "../dir/objects.json#/definitions/object"}},
    }
    test_boolean = {"type": "boolean"}
    test_one_of = {"oneOf": [{"$ref": "../dir/objects.json#/definitions/test_object"}]}
    test_all_of = {
        "allOf": [
            {"$ref": "../dir/objects.json#/definitions/test_object"},
            {"type": "object", "properties": {"test_property": {"type": "string"}}},
        ]
    }
    test_enum = {"type": "string", "enum": ["test_value"]}
    test_objects = {
        "test_object": test_object,
        "test_reference": test_reference,
        "test_array": test_array,
        "test_bool": test_boolean,
        "test_one_of": test_one_of,
        "test_all_of": test_all_of,
        "test_enum": test_enum,
    }
    result = parse_objects(test_objects)
    assert result == [
        ObjectSchema.from_dict("TestObject", test_object["properties"]),
        ReferenceSchema.from_dict("TestReference", test_reference),
        ArraySchema.from_dict("TestArray", test_array),
        BoolSchema.from_dict("TestBool", test_boolean),
        OneOfSchema.from_dict("TestOneOf", test_one_of["oneOf"]),
        AllOfSchema.from_dict("TestAllOf", test_all_of["allOf"]),
        get_enum_from_dict("TestEnum", test_enum),
    ]


def test_generate_classes(tmp_path: Path):
    test_object = ObjectSchema.from_dict("TestObject", {"test_property": {"type": "string"}})
    test_another_object = ObjectSchema.from_dict(
        "TestAnotherObject", {"test_property": {"type": "string"}}
    )
    test_objects = [test_object, test_another_object]
    output_path = tmp_path / "path" / "to" / "output"
    generate_classes(test_objects, output_path)
    objects_file = output_path / "objects.py"
    assert objects_file.exists()
    assert objects_file.read_text() == (
        f"{IMPORTS}" f"{test_object.to_class()}\n" f"{test_another_object.to_class()[:-1]}"
    )


def test_generate_classes_empty(tmp_path: Path):
    output_path = tmp_path / "path" / "to" / "output"
    generate_classes([], output_path)
    objects_file = output_path / "objects.py"
    assert objects_file.exists()
    assert objects_file.read_text() == f"{IMPORTS}"


def test_generate_objects(tmp_path_factory: pytest.TempPathFactory):
    test_object = {
        "test_object": {"type": "object", "properties": {"test_property": {"type": "string"}}}
    }
    # Create a temporary directory of the form /data/section/objects.json
    output_path = tmp_path_factory.mktemp("output")
    objects_path = tmp_path_factory.mktemp("data")
    section_path = objects_path / "section"
    section_path.mkdir()

    create_objects_file(section_path, test_object)
    generate_objects(objects_path, output_path)
