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

    def _get_description(self) -> str:
        if self.description is not None:
            string = f'    """\n    {self.description}\n'
        else:
            string = '    """\n'

        string += "    Patterns of dict (as regexp) in the form of key-value:\n"
        for pattern, field in self.patternProperties.items():
            string += f"    {pattern}: {field.__typehint__}\n"
        string += '    """\n'
        return string
