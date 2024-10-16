from nodeflow.node.abstract import Variable


class Float(Variable):
    def __init__(self, value: float):
        assert isinstance(value, float)
        super().__init__(value)

__all__ = [
    "Float"
]