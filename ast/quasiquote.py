from ast import Node, Name
from scope import Scope
from value import Value, Symbol


class Quasiquote(Node):

    def __init__(self, val: Node) -> None:
        self.body: Node = val

    def eval(self, env: Scope) -> Value:
        if isinstance(self.body, Name):
            return Symbol(self.body.identifier)
        return self.body.eval(env)

    def __str__(self) -> str:
        return f'{self.body}'
