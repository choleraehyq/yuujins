from ast import Node
from scope import Scope
from value import Value, String as StringValue


class String(Node):

    def __init__(self, val: str) -> None:
        self.val: str = val[1:-1]

    def eval(self, env: Scope) -> Value:
        return StringValue(self.val)

    def __str__(self) -> str:
        return f'"{self.val}"'
