from ast import Node
from value import Value, Promise
from scope import Scope


class Delay(Node):

    def __init__(self, expr: Node) -> None:
        self.expr: Node = expr

    def eval(self, env: Scope) -> Value:
        return Promise(env, self.expr)

    def __str__(self) -> str:
        return f'(delay {self.expr})'
