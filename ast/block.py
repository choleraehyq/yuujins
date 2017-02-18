from typing import List, Optional

from ast import Node
from value import Value, Promise
from scope import Scope


class Block(Node):

    def __init__(self, expr: List[Node]) -> None:
        self.exprs: List[Node] = expr

    def eval(self, env: Scope) -> Optional[Value]:
        if len(self.exprs) == 0:
            return None
        ret: Value
        for x in self.exprs:
            ret = x.eval(env)
        return ret

    def __str__(self) -> str:
        return ' '.join([str(x) for x in self.exprs])
