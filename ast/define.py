from typing import Optional

from ast import Node, Name
from value import Value
from scope import Scope
import binder


class Define(Node):

    def __init__(self, pattern: Name, val: Node) -> None:
        self.pattern: Name = pattern
        self.val: Node = val

    def eval(self, env: Scope) -> Optional[Value]:
        binder.define(env, self.pattern.identifier, self.val.eval(env))

    def __str__(self) -> str:
        return f'(define {self.pattern} {self.val})'