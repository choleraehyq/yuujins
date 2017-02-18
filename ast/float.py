from ast import Node
from value import Value, Float as FloatValue
from scope import Scope


class Float(Node):

    def __init__(self, s: str) -> None:
        self.val: float = float(s)


    def eval(self, env: Scope) -> Value:
        return FloatValue(self.val)

    def __str__(self) -> str:
        return str(self.val)