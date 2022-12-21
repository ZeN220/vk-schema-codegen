from __future__ import annotations

import logging
import time
from pathlib import Path

import msgspec

from src.parsers.objects.schemas import (
    AllOfSchema,
    ArraySchema,
    BaseSchema,
    BoolSchema,
    EnumSchema,
    ObjectSchema,
    OneOfSchema,
    ReferenceSchema,
)
from src.parsers.objects.schemas.enum import (
    get_enum_from_dict,
    get_enums_from_all_of,
    get_enums_from_object,
)
from src.strings import to_camel_case
from src.strings.validators import validate_order_references

logger = logging.getLogger(__name__)

IMPORTS = (
    "from __future__ import annotations\n\n"
    "import enum\n"
    "import typing\n\n"
    "import pydantic\n\n\n"
)


def generate_objects(input_dir: Path, output_dir: Path):
    start = time.time()
    logger.info("Generating objects...")
    schemas = get_objects(input_dir)

    logger.info("Parsing objects...")
    objects = parse_objects(schemas)
    logger.info("Found %s objects", len(objects))
    logger.info("Parsing objects finished.")

    logger.info("Generating classes...")
    generate_classes(objects, output_dir)
    logger.info("Generating classes finished")

    end = round(time.time() - start, 3)
    logger.info("Objects generation finished in %s seconds", end)


def get_objects(input_dir: Path) -> dict:
    schemas = {}
    for directory in input_dir.iterdir():
        file_dir = directory / "objects.json"
        if not file_dir.is_file():
            continue
        objects = msgspec.json.decode(file_dir.read_bytes())
        schemas.update(objects["definitions"])
    return schemas


def parse_objects(objects: dict) -> list[BaseSchema]:
    objects = validate_order_references(objects)
    objects_result: list[BaseSchema] = []
    for object_name, value in objects.items():
        result: BaseSchema
        object_name = to_camel_case(object_name)

        if value.get("type") == "array":
            result = ArraySchema.from_dict(object_name, value)
        elif value.get("type") == "boolean":
            result = BoolSchema.from_dict(object_name, value)
        elif value.get("oneOf") is not None:
            result = OneOfSchema.from_dict(object_name, value["oneOf"])
        elif value.get("enum") is not None:
            result = get_enum_from_dict(object_name, value)
        elif value.get("$ref") is not None:
            result = ReferenceSchema.from_dict(object_name, value)
        elif value.get("allOf") is not None:
            enums_from_properties = get_enums_from_all_of(object_name, value["allOf"])
            objects_result.extend(enums_from_properties)
            result = AllOfSchema.from_dict(object_name, value["allOf"])
        else:
            properties = value.get("properties", {})
            enums_from_properties = get_enums_from_object(object_name, properties)
            objects_result.extend(enums_from_properties)
            result = ObjectSchema.from_dict(object_name, properties)

        objects_result.append(result)
    return objects_result


def generate_classes(objects: list[BaseSchema], output_dir: Path) -> None:
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    # Because some objects may have fields with default value as enum, need to generate enums first
    objects = sorted(objects, key=lambda object_: isinstance(object_, EnumSchema), reverse=True)
    with open(output_dir / "objects.py", "w", encoding="utf-8") as file:
        file.write(IMPORTS)
        for obj in objects[:-1]:
            file.write(obj.to_class() + "\n")
        # Last object without empty line
        last_object = objects[-1]
        file.write(last_object.to_class()[:-1])
