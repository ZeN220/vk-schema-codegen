from src.properties import StringEnumProperty
from src.schemas import ResponseSchema


class TestResponseSchema:
    def test_from_dict(self):
        response = {"type": "integer"}
        schema = ResponseSchema.from_dict(name="TestName", response=response)

        assert schema.name == "TestName"
        assert schema.response.name == "response"
        assert schema.response.type == "integer"

    def test_from_dict_reference(self):
        response = {"properties": {}}
        schema = ResponseSchema.from_dict(name="TestName", response=response)

        assert schema.name == "TestName"
        assert schema.response.name == "response"
        assert schema.response.reference == "TestNameModel"

    def test_from_dict_enum(self):
        response = {"type": "string", "enum": ["test_value", "another_value"]}
        schema = ResponseSchema.from_dict(name="TestName", response=response)

        assert schema.name == "TestName"
        assert schema.response.name == "response"
        assert isinstance(schema.response, StringEnumProperty)
        assert schema.response.enum == ["test_value", "another_value"]

    def test_to_class(self):
        response = {"type": "integer", "required": True}
        schema = ResponseSchema.from_dict(name="TestName", response=response)
        class_string = schema.to_class()
        assert class_string == "class TestName(pydantic.BaseModel):\n" "    response: int\n\n"
