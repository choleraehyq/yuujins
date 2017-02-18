from typing import Optional

from ast import Node, Name
from scope import Scope
from value import Value
import binder
import constants


class Set(Node):

    def __init__(self, pattern: Name, val: Node) -> None:
        self.val: Node = val
        self.pattern: Name = pattern

    def eval(self, env: Scope) -> Optional[Value]:
        val: Value = self.val.eval(env)
        binder.assign(env, self.pattern.identifier, val)

    def __str__(self) -> str:
        return f'({constants.SET} {self.pattern} {self.val})'
