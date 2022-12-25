from .base import BaseField


class ArrayField(BaseField):
    type: str
    items: BaseField

    @property
    def __typehint__(self) -> str:
        return f"list[{self.items.__typehint__}]"

    def _get_description(self) -> str:
        if self.items.description is not None:
            return f'    """{self.items.description}"""\n'
        elif self.description is not None:
            return f'    """{self.description}"""\n'
        return ""

    def to_field_class(self):
        if self.required:
            string = self._get_required_field_class()
        else:
            string = self._get_optional_field_class()

        string += self._get_description()
        return string
