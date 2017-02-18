from typing import List

from ast import Node, Name
from scope import Scope
from value import Value
import binder

class LetStar(Node):

    def __init__(self, patterns: List[Name], exprs: List[Node], body: Node) -> None:
        self.patterns: List[Name] = patterns
        self.exprs: List[Node] = exprs
        self.body: Node = body

    def eval(self, env: Scope) -> Value:
        e: Scope = env
        for i, _ in enumerate(self.patterns):
            e = Scope(e)
            binder.define(e, self.patterns[i].identifier, self.exprs[i].eval(e))
        return self.body.eval(e)

    def __str__(self) -> str:
        bindings: str = ' '.join(['({} {})'.format(self.patterns[i], self.exprs[i]) for i in range(len(self.patterns))])
        return f'(let* ({bindings}) {self.body})'