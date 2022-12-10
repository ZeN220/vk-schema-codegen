from msgspec import Struct


class BaseSchema(Struct):
    name: str
