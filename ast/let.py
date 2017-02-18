from typing import List

from ast import Node, Name
from scope import Scope
from value import Value
import binder

class Let(Node):

    def __init__(self, patterns: List[Name], exprs: List[Node], body: Node) -> None:
        self.patterns: List[Name] = patterns
        self.exprs: List[Node] = exprs
        self.body: Node = body

    def eval(self, s: Scope) -> Value:
        env: Scope = Scope(s)
        ext: Scope = Scope(s)
        for i, _ in enumerate(self.patterns):
            binder.define(ext, self.patterns[i].identifier, self.exprs[i].eval(env))
        return self.body.eval(ext)

    def __str__(self) -> str:
        bindings: str = ' '.join(['({} {})'.format(self.patterns[i], self.exprs[i]) for i in range(len(self.patterns))])
        return f'(let ({bindings}) {self.body})'