from nodeflow.node.abstract import Variable


class Int(Variable):
    def __init__(self, value: int):
        assert isinstance(value, int)
        super().__init__(value)

__all__ = [
    "Int"
]