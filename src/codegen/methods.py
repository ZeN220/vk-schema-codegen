from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import msgspec

from src.schemas import MethodSchema

logger = logging.getLogger(__name__)


@dataclass
class SectionMethods:
    name: str
    methods: list[MethodSchema]
    imports: Iterable[str]


def generate_methods(input_dir: Path, output_dir: Path) -> None:
    start = time.time()
    logger.info("Generating methods...")

    end = round(time.time() - start, 3)
    logger.info("Methods generation finished in %s seconds", end)


def get_methods(input_dir: Path) -> dict:
    schemas = {}
    for directory in input_dir.iterdir():
        file_dir = directory / "methods.json"
        if not file_dir.is_file():
            continue
        data = msgspec.json.decode(file_dir.read_bytes())
        raw_methods = data["methods"]
        schemas.update(raw_methods)
    return schemas


def parse_methods() -> None:
    pass
