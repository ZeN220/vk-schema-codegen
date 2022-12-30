from .base import BaseProperty


class DictProperty(BaseProperty):
    type: str

    @property
    def __typehint__(self) -> str:
        return "dict"
