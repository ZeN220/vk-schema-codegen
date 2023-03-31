from src.properties import BaseProperty, ReferenceProperty, get_property
from src.strings import to_camel_case

from .base import BaseSchema


class ResponseSchema(BaseSchema):
    response: BaseProperty

    @classmethod
    def from_dict(cls, name: str, response: dict) -> "ResponseSchema":
        response_field: BaseProperty
        if response.get("properties") is not None:
            response_model = to_camel_case(name) + "Model"
            response_field = ReferenceProperty(name="response", reference=response_model)
        else:
            response_field = get_property(item=response, name="response", typehint=name + "Model")
        return cls(name=name, response=response_field)

    def to_class(self) -> str:
        response_field = self.response.to_field_class()
        class_string = f"class {self.name}(pydantic.BaseModel):\n" f"{response_field}\n"
        return class_string
