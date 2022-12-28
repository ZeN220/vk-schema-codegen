from src.schemas import BoolSchema


class TestBoolSchema:
    def test_from_dict(self):
        data = {"type": "boolean", "description": "Test description"}
        schema = BoolSchema.from_dict(name="TestName", data=data)
        assert schema.name == "TestName"
        assert schema.type == "boolean"
        assert schema.description == "Test description"

    def test_to_class(self):
        data = {"type": "boolean", "description": "Test description"}
        schema = BoolSchema.from_dict(name="TestName", data=data)
        class_string = schema.to_class()
        assert class_string == "TestName = bool  # Test description\n\n"
