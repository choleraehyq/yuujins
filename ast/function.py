from ast import Node, Name
from value import Value
from scope import Scope


class Function(Node):

    def __init__(self, caller: Name, body: Node) -> None:
        self.caller: Name = caller
        self.body: Node = body

    def eval(self, env: Scope) -> Value:
        return self.body.eval(env)

    def __str__(self) -> str:
        return f'{self.body}'
