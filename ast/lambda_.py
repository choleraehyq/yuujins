from typing import Optional

from ast import Node, NULL_PAIR
from scope import Scope
from value import Value, Closure
import binder

class Lambda(Node):

    def __init__(self, params: Optional[Node], body: Node) -> None:
        self.params: Optional[Node] = params
        self.body: Node = body
        if self.params is None:
            self.params = NULL_PAIR

    def eval(self, env: Scope) -> Value:
        return Closure(env, self)

    def __str__(self) -> str:
        return f'(lambda {self.params} {self.body})'