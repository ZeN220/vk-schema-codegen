from .base import BaseField


class DictField(BaseField):
    type: str

    @property
    def __typehint__(self) -> str:
        return "dict"
