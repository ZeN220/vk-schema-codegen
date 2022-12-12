from src.strings import get_reference, to_camel_case

from .base import BaseSchema


class ReferenceSchema(BaseSchema):
    reference: str

    @classmethod
    def from_dict(cls, name: str, data: dict):
        schema = cls(name=name, reference=data["$ref"])
        return schema

    def __str__(self):
        name = to_camel_case(self.name)
        reference = get_reference(self.reference)
        # fmt: off
        class_string = (
            f"class {name}({reference}):\n"
            f"    pass\n\n"
        )
        # fmt: on
        return class_string
