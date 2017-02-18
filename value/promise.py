from value import Value
from scope import Scope
from ast import Node

class Promise(Value):

    def __init__(self, env: Scope, lazy: Node) -> None:
        self.is_val, self.env, self.lazy = True, env, lazy

    def __str__(self) -> str:
        return '#<promise>'