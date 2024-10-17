from nodeflow.node.abstract import Function, Variable


class Sum(Function):
    def compute(self, lhs: Variable, rhs: Variable) -> Variable:
        return lhs.value + rhs.value

__all__ = [
    "Sum"
]