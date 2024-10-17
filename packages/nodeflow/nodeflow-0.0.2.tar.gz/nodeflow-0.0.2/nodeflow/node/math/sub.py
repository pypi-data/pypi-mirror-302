from nodeflow.node.abstract import Function, Variable


class Sub(Function):
    def compute(self, lhs: Variable, rhs: Variable) -> Variable:
        return lhs.value - rhs.value

__all__ = [
    "Sub"
]