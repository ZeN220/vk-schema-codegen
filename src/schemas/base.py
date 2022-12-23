from msgspec import Struct


class BaseSchema(Struct):
    name: str

    def to_class(self) -> str:
        raise NotImplementedError
