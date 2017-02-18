from ast import Node
from value import Value, Promise
from scope import Scope


class Begin(Node):

    def __init__(self, body: Node) -> None:
        self.body: Node = body

    def eval(self, env: Scope) -> Value:
        return self.body.eval(env)

    def __str__(self) -> str:
        if str(self.body) == '':
            return '(begin)'
        else:
            return f'(begin {self.body})'
