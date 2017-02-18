from typing import Optional

from ast import Node
from value import Value, Bool
from scope import Scope
import constants


class If(Node):

    def __init__(self, test: Node, then: Node, el: Optional[Node]) -> None:
        self.test: Node = test
        self.then: Node = then
        self.el: Optional[Node] = el

    def eval(self, env: Scope) -> Optional[Value]:
        re: Value = self.test.eval(env)
        if isinstance(re, Bool):
            if not re.val:
                if self.el == None:
                    return None
                else:
                    return self.el.eval(env)
        return self.then.eval(env)

    def __str__(self) -> str:
        return f'({constants.IF} {self.test} {self.then} {self.el})'