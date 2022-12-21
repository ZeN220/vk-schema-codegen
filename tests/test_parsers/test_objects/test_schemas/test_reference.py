from src.parsers.objects.schemas import ReferenceSchema


class TestReferenceSchema:
    def test_from_dict(self):
        schema = ReferenceSchema.from_dict(
            name="TestName", data={"$ref": "../dir/objects.json#/definitions/object"}
        )
        assert schema.name == "TestName"
        assert schema.reference == "../dir/objects.json#/definitions/object"

    def test_to_class(self):
        schema = ReferenceSchema.from_dict(
            name="TestName", data={"$ref": "../dir/objects.json#/definitions/object"}
        )
        class_string = schema.to_class()
        assert class_string == ("class TestName(Object):\n" "    pass\n\n")
