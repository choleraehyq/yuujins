from typing import List

from value import Value
from scope import Scope

class Node(Value):

    def eval(self, s: Scope) -> Value:
        pass


def eval_list(nodes: List[Node], s: Scope) -> List[Value]:
    return [node.eval(s) for node in nodes]
