from src.parsers.objects.schemas import AllOfSchema


class TestAllOfSchema:
    def test_from_dict(self):
        all_of = [
            {"$ref": "../dir/objects.json#/definitions/object"},
            {"$ref": "../dir/objects.json#/definitions/another_object"},
            {"properties": {"id": {"type": "integer"}}},
        ]
        schema = AllOfSchema.from_dict(name="TestName", all_of=all_of)
        assert schema.name == "TestName"
        assert schema.object_schema is not None
        assert len(schema.allOf) == 2
        assert schema.allOf[0].reference == "../dir/objects.json#/definitions/object"
        assert schema.allOf[1].reference == "../dir/objects.json#/definitions/another_object"

    def test_from_dict_without_object(self):
        all_of = [
            {"$ref": "../dir/objects.json#/definitions/object"},
            {"$ref": "../dir/objects.json#/definitions/another_object"},
        ]
        schema = AllOfSchema.from_dict(name="TestName", all_of=all_of)
        assert schema.name == "TestName"
        assert schema.object_schema is None
        assert schema.to_class() == "class TestName(Object, AnotherObject):\n    pass\n\n"

    def test_to_class(self):
        all_of = [
            {"$ref": "../dir/objects.json#/definitions/object"},
            {"$ref": "../dir/objects.json#/definitions/another_object"},
            {"properties": {"id": {"type": "integer"}}},
        ]
        schema = AllOfSchema.from_dict(name="TestName", all_of=all_of)
        class_string = schema.to_class()
        assert class_string == (
            "class TestName(Object, AnotherObject):\n" "    id: typing.Optional[int] = None\n\n"
        )

    def test_to_class_crutch(self):
        all_of = [
            {"$ref": "../wall/objects.json#/definitions/wall_carousel_base"},
            {"$ref": "../newsfeed/objects.json#/definitions/newsfeed_item_base"},
            {"$ref": "../wall/objects.json#/definitions/wall_wallpost_full"},
            {"properties": {"id": {"type": "integer"}}},
        ]
        schema = AllOfSchema.from_dict(name="NewsfeedItemWallpost", all_of=all_of)
        class_string = schema.to_class()
        assert class_string == (
            "class NewsfeedItemWallpost(NewsfeedItemBase, WallWallpostFull):\n"
            "    id: typing.Optional[int] = None\n\n"
        )
