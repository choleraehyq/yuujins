from ast import Node
from scope import Scope
from value import Value

class UnquoteSplicing(Node):

    def __init__(self, body: Node) -> None:
        self.body: Node = body

    def eval(self, env: Scope) -> Value:
        return self.body.eval(env)

    def __str__(self) -> str:
        return f',@{self.body}'
