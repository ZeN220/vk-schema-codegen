from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from src.schemas import BaseSchema


@dataclass
class ResponseSection:
    name: str
    imports: Iterable[str]
    responses: list[BaseSchema]
