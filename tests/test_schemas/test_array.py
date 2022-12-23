from src.fields import StringArrayItem
from src.schemas import ArraySchema


class TestArraySchema:
    def test_from_dict(self):
        schema = ArraySchema.from_dict(
            name="TestName", data={"type": "array", "items": {"type": "string"}}
        )
        assert schema.name == "TestName"
        assert schema.items == StringArrayItem(type="string")

    def test_to_class(self):
        schema = ArraySchema.from_dict(
            name="TestName",
            data={
                "type": "array",
                "items": {"type": "string"},
            },
        )
        class_string = schema.to_class()
        assert class_string == "TestName = list[str]\n\n"

    def test_to_class_with_description(self):
        schema = ArraySchema.from_dict(
            name="TestName",
            data={
                "type": "array",
                "items": {"type": "string"},
                "description": "Test description",
            },
        )
        class_string = schema.to_class()
        assert class_string == "TestName = list[str]  # Test description\n\n"
