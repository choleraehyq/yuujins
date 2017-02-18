from typing import List, Optional

from ast import Node
from scope import Scope
from value import Value


class Tuple(Node):

    def __init__(self, elements: List[Node]) -> None:
        self.elements: List[Node] = elements

    def eval(self, env: Scope) -> Optional[Value]:
        raise NotImplementedError('unsupported tuple evaluation')

    def __str__(self) -> str:
        return '({})'.format(' '.join([str(x) for x in self.elements]))

