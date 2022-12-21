from src.parsers.objects.schemas import ObjectSchema


class TestObjectSchema:
    def test_from_dict(self):
        properties = {
            "id": {"type": "integer"},
            "name": {"type": "string"},
        }
        schema = ObjectSchema.from_dict(name="TestName", properties=properties)
        assert schema.name == "TestName"
        assert len(schema.properties) == 2
        assert schema.properties[0].name == "id"
        assert schema.properties[0].type == "integer"
        assert schema.properties[1].name == "name"
        assert schema.properties[1].type == "string"

    def test_to_class(self):
        properties = {
            "id": {"type": "integer", "required": True},
            "name": {"type": "string"},
        }
        schema = ObjectSchema.from_dict(name="TestName", properties=properties)
        class_string = schema.to_class()
        assert class_string == (
            "class TestName(pydantic.BaseModel):\n"
            "    id: int\n"
            "    name: typing.Optional[str] = None\n\n"
        )

    def test_to_class_empty(self):
        properties = {}
        schema = ObjectSchema.from_dict(name="TestName", properties=properties)
        class_string = schema.to_class()
        assert class_string == "class TestName(pydantic.BaseModel):\n    pass\n\n"
