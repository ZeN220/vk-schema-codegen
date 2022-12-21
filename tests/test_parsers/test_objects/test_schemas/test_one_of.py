from src.parsers.objects.schemas.one_of import ElementOneOf, OneOfSchema, ReferenceOneOf


class TestOneOfSchema:
    def test_from_dict(self):
        one_of = [
            {"$ref": "../dir/objects.json#/definitions/object"},
            {"type": "string"},
        ]
        schema = OneOfSchema.from_dict(name="TestName", one_of=one_of)
        assert schema.name == "TestName"
        assert schema.oneOf[0] == ReferenceOneOf(
            reference="../dir/objects.json#/definitions/object"
        )
        assert schema.oneOf[1] == ElementOneOf(type="str")

    def test_to_class(self):
        schema = OneOfSchema.from_dict(
            name="TestName",
            one_of=[
                {"$ref": "../dir/objects.json#/definitions/object"},
                {"type": "string"},
            ],
        )
        class_string = schema.to_class()
        assert class_string == "TestName = typing.Union[Object, str]\n\n"

    def test_to_class_long(self):
        schema = OneOfSchema.from_dict(
            name="TestName",
            one_of=[
                {"$ref": "../dir/objects.json#/definitions/VeryLongObjectName"},
                {"$ref": "../dir/objects.json#/definitions/AnotherVeryLongObjectName"},
                {"$ref": "../dir/objects.json#/definitions/VeryVeryLongObjectName"},
                {"$ref": "../dir/objects.json#/definitions/AnotherVeryVeryLongObjectName"},
            ],
        )
        class_string = schema.to_class()
        assert class_string == (
            "TestName = typing.Union[\n"
            "    VeryLongObjectName,\n"
            "    AnotherVeryLongObjectName,\n"
            "    VeryVeryLongObjectName,\n"
            "    AnotherVeryVeryLongObjectName\n"
            "]\n\n"
        )
