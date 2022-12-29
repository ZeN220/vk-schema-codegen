from __future__ import annotations

from .base import BaseField


class PatternField(BaseField):
    type: str
    patternProperties: dict[str, BaseField]
    additionalProperties: bool

    @property
    def __typehint__(self) -> str:
        typehints = [field.__typehint__ for field in self.patternProperties.values()]
        types = ", ".join(typehints)
        if len(typehints) == 1:
            return f"dict[str, {types}]"
        return f"dict[str, typing.Union[{types}]]"

    def _get_description(self) -> dict:
        description_object = super()._get_description()
        string = "Patterns of dict keys (as regexp)"
        patterns = [pattern for pattern in self.patternProperties.keys()]
        description_object[string] = ", ".join(patterns)
        return description_object
