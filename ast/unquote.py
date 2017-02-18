from ast import Node, Name
from scope import Scope
from value import Value, Symbol


class Unquote(Node):

    def __init__(self, body: Node) -> None:
        self.body: Node = body

    def eval(self, env: Scope) -> Value:
        if isinstance(self.body, Name):
            return Symbol(self.body.identifier)
        return self.body.eval(env)

    def __str__(self) -> str:
        return f'\'{self.body}'
