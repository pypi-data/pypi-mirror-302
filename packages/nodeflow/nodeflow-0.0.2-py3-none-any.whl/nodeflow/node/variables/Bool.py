from nodeflow.node.abstract import Variable


class Bool(Variable):
    def __init__(self, value: bool):
        assert isinstance(value, bool)
        super().__init__(value)

__all__ = [
    "Bool"
]