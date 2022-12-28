from src.fields import (
    BaseField,
    ReferenceField,
    get_enum_field_from_dict,
    get_field_from_dict,
)
from src.strings import to_camel_case

from .base import BaseSchema


class ResponseSchema(BaseSchema):
    response: BaseField

    @classmethod
    def from_dict(cls, name: str, response: dict):
        response_field: BaseField
        if response.get("properties") is not None:
            response_model = to_camel_case(name) + "Model"
            response_field = ReferenceField(name="response", reference=response_model)
        else:
            if response.get("enum") is not None:
                response_field = get_enum_field_from_dict(
                    name="response", item=response, typehint=name + "Model"
                )
            else:
                response_field = get_field_from_dict(name="response", item=response)
        return cls(name=name, response=response_field)

    def to_class(self) -> str:
        response_field = self.response.to_field_class()
        class_string = f"class {self.name}(pydantic.BaseModel):\n" f"{response_field}\n"
        return class_string
