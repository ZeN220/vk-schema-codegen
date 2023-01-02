from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import msgspec

from src.schemas import BaseSchema, ObjectSchema, ResponseSchema
from src.schemas.enum import get_enum_from_dict, get_enums_from_object
from src.strings import parse_responses_references, to_camel_case

logger = logging.getLogger(__name__)


@dataclass
class ResponseSection:
    name: str
    imports: Iterable[str]
    responses: list[BaseSchema]


def generate_responses(input_dir: Path, output_dir: Path, objects_package: str) -> None:
    start = time.time()
    logger.info("Generating responses...")
    schemas = get_responses(input_dir)

    generate_classes(schemas, output_dir, objects_package)

    end = round(time.time() - start, 3)
    logger.info("Responses generation finished in %s seconds", end)


def get_responses(input_dir: Path) -> list[ResponseSection]:
    schemas = []
    for directory in input_dir.iterdir():
        file_dir = directory / "responses.json"
        if not file_dir.is_file():
            continue
        objects = msgspec.json.decode(file_dir.read_bytes())
        objects = objects["definitions"]
        imports = parse_responses_references(objects)
        result = parse_responses(objects)
        section = ResponseSection(name=directory.name, responses=result, imports=imports)
        schemas.append(section)
    return schemas


def parse_responses(schemas: dict[str, dict]) -> list[BaseSchema]:
    responses_result: list[BaseSchema] = []
    for response_name, value in schemas.items():
        response_name = to_camel_case(response_name)
        response = value["properties"]["response"]

        if response.get("properties") is not None:
            object_name = response_name + "Model"
            properties = response["properties"]

            enums_from_object = get_enums_from_object(object_name, properties)
            responses_result.extend(enums_from_object)

            response_object = ObjectSchema.from_dict(object_name, properties)
            responses_result.append(response_object)
        elif response.get("enum") is not None:
            enum_response = response.copy()
            enum_response.pop("required")
            enum = get_enum_from_dict(response_name + "Model", enum_response)
            responses_result.append(enum)

        obj = ResponseSchema.from_dict(response_name, response)
        responses_result.append(obj)
    return responses_result


def generate_classes(
    schemas: list[ResponseSection], output_dir: Path, objects_package: str
) -> None:
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    for schema in schemas:
        classes = ""
        for response in schema.responses:
            classes += response.to_class() + "\n"

        sort_imports = sorted(schema.imports)
        imports = _get_imports(classes, sort_imports, objects_package)

        filename = schema.name + ".py"
        with open(output_dir / filename, "w", encoding="utf-8") as file:
            # classes[:-2] - remove last 2 new lines
            file.write(imports + classes[:-2])


def _get_imports(classes: str, objects_imports: Iterable[str], objects_package: str) -> str:
    imports = "from __future__ import annotations\n\n"
    if classes.find("enum.") != -1:
        imports += "import enum\n"
    if classes.find("typing.") != -1:
        imports += "import typing\n\n"
    else:
        imports += "\n"

    imports += "import pydantic\n\n"
    if objects_imports:
        imports += f"from {objects_package}.objects import (\n"
        for obj in objects_imports:
            imports += f"    {obj},\n"
        imports += ")\n\n"
    imports += "\n"
    return imports
