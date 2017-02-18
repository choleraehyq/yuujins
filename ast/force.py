from typing import Optional

from ast import Node
from value import Value, Promise
from scope import Scope


class Force(Node):

    def __init__(self, promise: Node) -> None:
        self.promise: Node = promise

    def eval(self, s: Scope) -> Optional[Value]:
        val = self.promise.eval(s)
        if isinstance(val, Promise):
            if not val.is_val:
                return None
            else:
                val.is_val = False
                env: Scope = val.env
                lazy: Node = val.lazy
                return lazy.eval(env)
        else:
            raise TypeError(f'force: expected argument of type <promise>, given: {val}')

    def __str__(self) -> str:
        return f'(force {self.promise})'